import os

flask_app_config = {
    "debug": os.environ.get("FLUSK_DEBUG_OPTION", True),
    "host": os.environ.get("FLASK_HOST", "0.0.0.0"),
    "port": os.environ.get("FLASK_PORT", 5000),
    "ssl_context": os.environ.get("CONTEXT", "adhoc"),
}


class Config:
    # Configurazione generica per l'app Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "mysecretkey")

