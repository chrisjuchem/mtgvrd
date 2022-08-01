import trafaret as t

user_update_trafaret = t.Dict(
    {
        t.Key("username", optional=True): t.String(32),
    }
)
