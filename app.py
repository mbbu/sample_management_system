import os

import app as app

from api import create_app
from flask_cors import CORS

debug = True

CORS(app, resources={r'/*': {'origins': '*'}})

# Bind to $PORT if defined, otherwise default to 5000.
port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=port
    )


