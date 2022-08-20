import trafaret as t

from app.server.enums import UserDraftRelationship
from app.server.trafarets.utils import UUID, base_list_trafaret

MIN_SEATS = 1
MAX_SEATS = 16
MIN_ROUNDS = 1
MAX_ROUNDS = 100

create_draft_trafaret = t.Dict(
    {
        t.Key("name"): t.String(64),
        t.Key("seats", to_name="n_seats"): t.Int(gte=MIN_SEATS, lte=MAX_SEATS),
        t.Key("rounds"): t.Int(gte=MIN_ROUNDS, lte=MAX_ROUNDS),
        t.Key("multiseat", default=False): t.ToBool,
        t.Key("random_seats", default=True): t.ToBool,
    }
)

join_draft_trafaret = t.Dict({t.Key("seat_no", optional=True): t.Int(gte=0)})

pick_trafaret = t.Dict(
    {
        t.Key("card_id"): UUID,
        t.Key("pick_no"): t.Int(gte=0),
    }
)

list_draft_trafaret = base_list_trafaret + t.Dict(
    {
        t.Key("filter", optional=True): t.Enum(*UserDraftRelationship.ALL),
    }
)
