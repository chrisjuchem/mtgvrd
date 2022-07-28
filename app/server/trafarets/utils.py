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
