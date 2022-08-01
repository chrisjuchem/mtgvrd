import trafaret as t

redirect_trafaret = t.Dict({t.Key("back_to", optional=True): t.String(allow_blank=True)})

callback_trafaret = t.Dict(
    {
        t.Key("code"): t.String,
        t.Key("state"): t.String,
    }
)
