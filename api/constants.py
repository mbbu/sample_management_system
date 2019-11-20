# App Info
APP_NAME = 'SAMPLE_MANAGEMENT_SYSTEM'

# Config
APP_CONFIG_ENV_VAR = APP_NAME + "_CONFIG"
DEV_CONFIG_VAR = "development"
PROD_CONFIG_VAR = "production"

# Database
DATABASE_URI_ENV_NAME = APP_NAME + "_DATABASE_URI"

# Logging Format
from api.config import RequestFormatter
AppLoggingFormat = RequestFormatter(
        '[%(asctime)s] Remote Address:%(remote_addr)s requested %(url)s\n'
        ' [%(levelname)s]: %(message)s [in %(pathname)s::%(lineno)d]\n'
    )

# External URLs and APIs
