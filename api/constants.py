# App Info
from datetime import timedelta

import redis

APP_NAME = 'SAMPLE_MANAGEMENT_SYSTEM'

# Config
APP_CONFIG_ENV_VAR = APP_NAME + "_CONFIG"
DEV_CONFIG_VAR = "development"
PROD_CONFIG_VAR = "production"
SECRET_KEY = APP_NAME + '_SECRET_KEY'

# Redis
ACCESS_EXPIRES = timedelta(days=7)
REFRESH_EXPIRES = timedelta(days=30)

revoked_store = redis.StrictRedis(host='localhost', port=6379, db=0,
                                  decode_responses=True)

# Database
DATABASE_URI_ENV_NAME = APP_NAME + "_DATABASE_URI"

# External URLs and APIs
REDCAP_URI = 'https://redcap.icipe.org/api/'

# Variable
DATE_TIME_NONE = '0001-01-01 00:00'
