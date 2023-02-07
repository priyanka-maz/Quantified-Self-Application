from application.api import *
import os
from flask import Flask
from flask_restful import Api
from flask_security.core import Security
from flask_security.datastore import SQLAlchemySessionUserDatastore
from application.config import *
from application.database import db
from application.jobs import workers
from application.models import User, Role
from flask_login import LoginManager
from flask_security import utils
from flask_sse import sse
from flask_caching import Cache

app = None
api = None
celery = None
cache = None

def create_app():
    app = Flask(__name__, template_folder="templates")

    if os.getenv("ENV", "development") == "production":
        print("Starting Production Server")
        app.config.from_object(ProductionConfig)
    else:
        print("Starting Development Server")
        app.config.from_object(DevelopmentConfig)

    print("DB Initialization")
    db.init_app(app)
    print("DB Init is complete")
    app.app_context().push()
    app.logger.info("App setup is complete")

    # Setup Flask-Security
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)

    api = Api(app)
    app.app_context().push()

    # Create celery
    celery = workers.celery

    # Update with configuration
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"],
        timezone = app.config["CELERY_TIMEZONE"]
    )
    celery.Task = workers.ContextTask
    app.app_context().push()
    cache = Cache(app)
    app.app_context().push()
    return app, api, security, cache, celery


app, api, security, cache, celery = create_app()


@app.route('/service-worker.js')
def root_worker():
    return app.send_static_file('service-worker.js')

@app.before_first_request
def before_first_request():
    db.create_all()

@app.after_request
def add_header(response):
    """
    Add headers to cache the rendered page for 10 minutes.
    """
    response.headers['Cache-Control'] = 'max-age=604800, must-revalidate'
    return response

# Import all the controllers so they are loaded
from application.controllers import *


# Import all restful controllers
api.add_resource(UserAPI, "/api/user")
api.add_resource(TrackerAPI, "/api/tracker")
api.add_resource(LogAPI, "/api/log")

if __name__ == '__main__':
    # Run the Flask app
    app.run(host="0.0.0.0", port=8080)
