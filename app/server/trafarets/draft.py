import trafaret as t

from app.server.enums import UserDraftRelationship
from app.server.trafarets.utils import UUID, base_list_trafaret

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

list_draft_trafaret = base_list_trafaret + t.Dict(
    {
        t.Key("filter", optional=True): t.Enum(*UserDraftRelationship.ALL),
    }
)
