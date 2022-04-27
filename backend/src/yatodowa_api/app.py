import os
from pathlib import Path
from typing import Optional

import yaml
from flask import Flask
from flask_migrate import Migrate

from yatodowa_api.components.collections.controller import collections_api
from yatodowa_api.components.groups.controller import groups_api
from yatodowa_api.components.tasks.controller import tasks_api
from yatodowa_api.sqldb.core import get_db


def create_app(custom_config_dirpath: Optional[str] = None) -> Flask:
    app = Flask(__name__)

    app_config_dirpath = Path(
        custom_config_dirpath
        or os.getenv("APP_CONFIG_DIR", None)
        or Path(app.root_path).parent.parent.parent / "config" / "local"
    )

    app.config.from_file(str(app_config_dirpath / "flask.yml"), load=yaml.safe_load)

    db = get_db()
    db.init_app(app)
    migrate = Migrate(
        app,
        db,
        directory=Path(os.path.realpath(__file__)).parent / "sqldb" / "migrations",
    )

    app.register_blueprint(tasks_api)
    app.register_blueprint(collections_api)
    app.register_blueprint(groups_api)

    return app
