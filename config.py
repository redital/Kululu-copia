import os

flask_app_config = {
    "debug": os.environ.get("FLUSK_DEBUG_OPTION", True),
    "host": os.environ.get("FLASK_HOST", "127.0.0.1"),
    "port": os.environ.get("FLASK_PORT", 5000),
    "ssl_context": os.environ.get("CONTEXT", "adhoc"),
    "allow_unsafe_werkzeug ": os.environ.get("UNSAFE_WERKZEUG ", "True"),
}


class Config:
    # Configurazione generica per l'app Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "mysecretkey")

