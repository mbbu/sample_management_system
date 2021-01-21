# App Info
import os
from datetime import timedelta

import redis

APP_NAME = 'SAMPLE_MANAGEMENT_SYSTEM'

# Config
APP_CONFIG_ENV_VAR = APP_NAME + "_CONFIG"
DEV_CONFIG_VAR = "development"
PROD_CONFIG_VAR = "production"
SECRET_KEY = APP_NAME + '_SECRET_KEY'
SECURITY_PASSWORD_SALT = APP_NAME + '_SECURITY_PASSWORD_SALT'

# Redis
ACCESS_EXPIRES = timedelta(days=7)
REFRESH_EXPIRES = timedelta(days=30)

revoked_store = redis.StrictRedis(host='localhost', port=6379, db=0,
                                  decode_responses=True)

# Database
DATABASE_URI_ENV_NAME = APP_NAME + "_DATABASE_URI"

# External URLs and APIs
REDCAP_URI = 'https://redcap.icipe.org/redcap/api/'
EMAIL_CONFIRM_URI = 'http://lims.icipe.org:8080/confirm/{0}'
PASSWORD_RESET_URI = 'http://lims.icipe.org:8080/reset/{0}'
SAMPLE_REQUEST_RESPONSE = 'http://lims.icipe.org:8080/request-response/{0}'
SAMPLE_COLLECTION_FORM = 'https://redcap.icipe.org/redcap/surveys/?s=EAC9JMJWWT'
SAMPLE_MANAGEMENT_FORM = 'https://redcap.icipe.org/redcap/surveys/?s=3LWMHELP7P'

# Variable
DATE_TIME_NONE = '0001-01-01 00:00'

# Email token valid duration
EMAIL_TOKEN_EXPIRATION = 3600  # equivalent to 1 hour
EXPIRATION_AS_HR = EMAIL_TOKEN_EXPIRATION / (60 * 60)

# Email sender
EMAIL_SENDER = 'icipe.samplemanagementsystem@gmail.com'

# role constants
SYSADMIN = "-1"
THEMEADMIN = "1"

FORBIDDEN_FUNCTION_ACCESS_RESPONSE_CODE = 403
FORBIDDEN_FUNCTION_ACCESS_RESPONSE = "You cannot access this function, you are not an admin!"

# sample status constants
SAMPLE_IN_LAB = 'COMPLETE'
SAMPLE_FROM_FIELD = 'INCOMPLETE'

# sample request constants
PENDING_STATUS = 'PENDING'
APPROVED_STATUS = 'APPROVED'
DECLINED_STATUS = 'DECLINED'

# Other non-sensitive token expiration
TOKEN_EXPIRATION = 36000  # approximately 10 days
TOKEN_EXPIRATION_AS_DAYS = int(TOKEN_EXPIRATION / (60 * 60))

basedir = os.path.abspath(os.path.dirname(__file__))
