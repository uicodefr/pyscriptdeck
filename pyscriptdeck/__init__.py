import logging
import logging.config
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pyscriptdeck.config import getconfig

load_dotenv()
logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)
db = SQLAlchemy()

def create_app(test_config=None, base_path=Path(__file__).parent.parent) -> Flask:
    # 1. Create App
    created_app = Flask(__name__)

    # 2. Config
    config = getconfig()
    if not created_app.secret_key:
        created_app.secret_key = os.environ.get("FLASK_SECRET_KEY")

    application_root = os.environ.get("APPLICATION_ROOT")
    if application_root:
        created_app.config["APPLICATION_ROOT"] = application_root

    if config["app.databasePath"].startswith("/"):
        database_abspath = Path(config["app.databasePath"])
    else:
        database_abspath = base_path.joinpath(config["app.databasePath"])
    created_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(database_abspath.resolve())
    created_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is not None:
        created_app.config.update(test_config)

    # 3. SQLAlchemy
    db.init_app(created_app)

    # 4. Init Controller and Main
    from pyscriptdeck import controller
    from pyscriptdeck.main import Main
    main = Main()
    controller.init_app(created_app, main)

    # 5. Init db
    with created_app.app_context():
        db.create_all()
        from pyscriptdeck.dao import UserDao, ParameterDao
        UserDao.create_adminuser_if_necessary()
        ParameterDao.init()

    logger.info("PyScriptDeck started")
    return created_app
