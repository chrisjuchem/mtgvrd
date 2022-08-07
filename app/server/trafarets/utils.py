from uuid import UUID as UUID_

import trafaret as t


# Simply adding ` | t.Null` to a trafaret results in confusing error messages
class Nullable(t.Trafaret):
    def __init__(self, trafaret):
        self.trafaret = trafaret

    def check_value(self, value):
        try:
            return t.Null().check(value=value)
        except t.DataError:
            return self.trafaret(value)


class UUID(t.String):
    def check_value(self, value):
        try:
            UUID_(super().check_and_return(value))
        except ValueError as exc:
            raise t.DataError("invalid UUID format") from exc


def HelpfulEnum(values=[], field="value"):  # pylint: disable=dangerous-default-value,invalid-name
    return t.OnError(t.Enum(*values), "value is not a valid {}".format(field))


base_list_trafaret = t.Dict(
    {
        # add one to the limit to easily check if the query has more or not
        t.Key("limit", default=50): t.ToInt(gte=0, lte=100) >> (lambda n: n + 1),
        t.Key("offset", default=0): t.ToInt(gte=0),
    }
)
