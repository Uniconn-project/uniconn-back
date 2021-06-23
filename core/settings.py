state = "dev"

if state == "prod":
    from .settings_prod import *
elif state == "dev":
    from .settings_dev import *
