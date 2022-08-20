from flask import Blueprint, g
from flask_sqlalchemy_session import current_session
from sqlalchemy import func

from app.db.models import Card, Draft, Pick, Seat
from app.server.decorators.auth import login_required
from app.server.decorators.validation import validate
from app.server.enums import ParamSources, StatusCodes, UserDraftRelationship
from app.server.formatters.draft import format_draft, format_seat
from app.server.formatters.list import format_list
from app.server.trafarets.draft import (
    create_draft_trafaret,
    join_draft_trafaret,
    list_draft_trafaret,
    pick_trafaret,
)

draft_routes = Blueprint("Draft", __name__)


@draft_routes.route("/new", methods=["POST"])
@login_required
@validate(ParamSources.JSON, create_draft_trafaret)
def new_draft(validated_data):
    draft = Draft.from_dict(validated_data)
    draft.owner = g.current_user
    current_session.add(draft)
    current_session.commit()

    return format_draft(draft), StatusCodes.HTTP_201_CREATED


@draft_routes.route("/")
@validate(ParamSources.QUERY_ARGS, list_draft_trafaret)
def list_drafts(validated_data):
    limit = validated_data["limit"]
    offset = validated_data["offset"]
    filter_ = g.current_user and validated_data.get("filter")

    query = Draft.query()
    if g.current_user:
        if filter_ == UserDraftRelationship.OWNER:
            query = query.filter(Draft.owner == g.current_user)
        if filter_ == UserDraftRelationship.PARTICIPANT:
            query = query.filter(Draft.players.contains(g.current_user))
    query = query.limit(limit).offset(offset).order_by(Draft.created_ts.desc())
    return format_list(query.all(), format_draft, limit)


@draft_routes.route("/<record(model=Draft):draft>")
def get_draft(draft):
    return format_draft(draft)


@draft_routes.route("/<record(model=Draft):draft>/join", methods=["POST"])
@login_required
@validate(ParamSources.JSON, join_draft_trafaret)
def join_draft(validated_data, draft):
    if len(draft.seats) >= draft.n_seats:
        return {"error": "Draft is full"}, StatusCodes.HTTP_409_CONFLICT
    if not draft.multiseat and g.current_user in draft.players:
        return {"error": "You already joined this draft"}, StatusCodes.HTTP_409_CONFLICT

    seat_no = validated_data.get("seat_no")
    if draft.random_seats or seat_no is None:
        seat_no = draft.next_seat_no
    elif seat_no >= draft.n_seats:
        return {
            "errors": {"seat_no": f"Must be less than {draft.n_seats}"}
        }, StatusCodes.HTTP_422_UNPROCESSABLE_ENTITY

    if seat_no in [seat.seat_no for seat in draft.seats]:
        return {"error": "Seat is already filled"}, StatusCodes.HTTP_409_CONFLICT

    seat = Seat.from_dict(
        {
            "draft_id": draft.id,
            "seat_no": seat_no,
            "player_id": g.current_user.id,
        }
    )
    draft.seats.append(seat)
    draft.save()
    return format_seat(seat), StatusCodes.HTTP_201_CREATED


@draft_routes.route("/<record(model=Draft):draft>/start", methods=["POST"])
@login_required
def start_draft(draft):
    if draft.owner != g.current_user:
        return {"error": "Only the owner can start the draft"}, StatusCodes.HTTP_403_FORBIDDEN
    if draft.start_ts:
        return {"error": "Draft already started"}, StatusCodes.HTTP_409_CONFLICT
    if len(draft.seats) != draft.n_seats:
        return {"error": "Draft not full"}, StatusCodes.HTTP_409_CONFLICT

    # Shuffle seats and start the draft
    # TODO shuffle seats
    draft.start_ts = func.now()
    draft.save()
    return format_draft(draft), StatusCodes.HTTP_200_OK


@draft_routes.route("/<record(model=Draft):draft>/pick", methods=["POST"])
@login_required
@validate(ParamSources.JSON, pick_trafaret)
def submit_pick(validated_data, draft):
    if not draft.start_ts:
        return {"error": "Draft is not started"}, StatusCodes.HTTP_409_CONFLICT

    pick_no = validated_data["pick_no"]
    seat = draft.seat_for_pick_no(pick_no)
    if pick_no >= draft.max_picks:
        return (
            {"errors": {"pick_no": f"Must be less than {draft.max_picks}"}},
            StatusCodes.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    if pick_no < draft.picks_made:
        return (
            {"errors": {"pick_no": "Already finalized"}},
            StatusCodes.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    if seat.player != g.current_user:
        return {
            "error": "You cannot make picks for seats that are not yours"
        }, StatusCodes.HTTP_403_FORBIDDEN

    card = Card.lookup_by_id(validated_data["card_id"])
    if not card:
        return {"errors": {"card_id": "Not found"}}, StatusCodes.HTTP_404_NOT_FOUND
    if not card.vrd_legal:
        return {"errors": {"card_id": "Card is illegal"}}, StatusCodes.HTTP_422_UNPROCESSABLE_ENTITY

    pick = Pick.from_dict(
        {
            "draft_id": draft.id,
            "seat_id": seat.id,
            "pick_no": pick_no,
            "round": pick_no // draft.rounds,
            "card_id": card.oracle_id,
            "pick_ts": func.now(),
        }
    )
    pick = current_session.merge(pick)

    if pick_no == draft.picks_made:
        draft.finalize_picks()

    current_session.commit()
    current_session.refresh(draft)

    return format_draft(draft), StatusCodes.HTTP_201_CREATED
