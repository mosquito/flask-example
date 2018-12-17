import os
import logging
from argparse import ArgumentParser
from contextlib import suppress

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from gevent.pywsgi import WSGIServer

from .models import Base
from .app import app


log = logging.getLogger()

CURRENT_DIR = os.path.abspath(os.getcwd())
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(MODULE_DIR, 'static')
TEMPLATES_PATH = os.path.join(MODULE_DIR, 'templates')

DEFAULT_DATABASE = "sqlite:////{}".format(
    os.path.join(CURRENT_DIR, 'db.sqlite3').lstrip("/")
)

parser = ArgumentParser()
parser.add_argument("-d", "--debug", action='store_true', help="Enable Flask debugger")
parser.add_argument("-L", "--listen", default='127.0.0.1', help="Listen this address for HTTP")
parser.add_argument("-P", "--port", default=8000, help="Listen this port for HTTP", type=int)
parser.add_argument("-D", "--db", default=DEFAULT_DATABASE, help="Database url (default: {})".format(DEFAULT_DATABASE))
parser.add_argument('--log-level', help='Set logging level', default='info',
                    choices=('critical', 'fatal', 'error', 'warning', 'warn', 'info', 'debug'))


def init_db():
    engine = create_engine(app.config['DATABASE'], convert_unicode=True)

    db_session = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )
    )

    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    app.db = db_session


def main():
    options = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, options.log_level.upper(), logging.INFO),
        format="[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s %(message)s"
    )

    app.config['DATABASE'] = options.db

    init_db()

    app.template_folder = TEMPLATES_PATH
    app.static_folder = STATIC_PATH

    log.info("Starting service on http://%s:%d/", options.listen, options.port)

    if options.debug:
        log.warning("Running on debug mode not for production.")
        app.run(host=options.listen, port=options.port, debug=True)
    else:
        http_server = WSGIServer((options.listen, options.port), app)

        with suppress(KeyboardInterrupt):
            http_server.serve_forever()
