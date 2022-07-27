import trafaret as t

from app.server.trafarets.utils import UUID

create_draft_trafaret = t.Dict(
    {
        t.Key("name"): t.String(64),
        t.Key("seats", to_name="n_seats"): t.Int(gte=2, lte=16),
        t.Key("rounds"): t.Int(gte=1, lte=100),
    }
)

# join_draft_trafaret = t.Dict({
#     t.Key
# })

pick_trafaret = t.Dict(
    {
        t.Key("card_id"): UUID,
        t.Key("pick_no"): t.Int(gte=0),
    }
)
