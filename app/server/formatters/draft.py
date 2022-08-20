from flask import g

from app.server.formatters.user import format_user


def format_draft(draft):
    return {
        "id": draft.id,
        "name": draft.name,
        "owner": format_user(draft.owner),
        "created_at": draft.created_ts and draft.created_ts.isoformat(),
        "started_at": draft.start_ts and draft.start_ts.isoformat(),
        "seats": draft.n_seats,
        "rounds": draft.rounds,
        "pick_order": draft.pick_order,
        "format": draft.format,
        "multiseat": draft.multiseat,
        "random_seats": draft.random_seats,
        "picks_completed": draft.picks_made,
        "players": [format_seat(s) for s in draft.seats],
        "picks": [format_pick(p) for p in draft.finalized_picks],
        "preloads": [format_pick(p) for p in draft.preloads_for(g.current_user)],
    }


def format_seat(seat):
    return {
        "id": seat.id,
        "seat_no": seat.seat_no,
        "player": format_user(seat.player),
    }


def format_pick(pick):
    return {
        "seat_id": pick.seat_id,
        "card_id": pick.card_id,
        "card_name": pick.card.name,
        "card_img": pick.card.image_uri,
        "pick_no": pick.pick_no,
        "round": pick.round,
    }
