def format_draft(draft):
    ret = {
        "id": draft.id,
        "name": draft.name,
        "started_at": draft.start_ts,
        "seats": draft.n_seats,
        "rounds": draft.rounds,
        "pick_order": draft.pick_order,
        "picks_completed": draft.picks_made,
        "players": [format_seat(s) for s in draft.seats],
        "picks": [format_pick(p) for p in draft.finalized_picks],
    }

    preloads = draft.seat_preloads()  # TODO swap to current user
    if preloads:
        ret["preloads"] = [format_pick(p) for p in preloads]

    return ret


def format_seat(seat):
    return {
        "id": seat.id,
        "seat_no": seat.seat_no,
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
