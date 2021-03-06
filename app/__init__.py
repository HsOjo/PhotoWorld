import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from . import common


class Application(Flask):
    def __init__(self):
        super().__init__(__name__)

        program_path = os.path.join(self.root_path, '..')
        self.config.from_pyfile('%s/config.py' % program_path)
        os.makedirs('%s/data' % program_path, exist_ok=True)

        common.current_app = self
        db.init_app(self)
        bootstrap.init_app(self)
        bootstrap_cdns = self.extensions['bootstrap']['cdns']
        bootstrap_cdns['bootstrap'] = bootstrap_cdns['local']
        bootstrap_cdns['jquery'] = bootstrap_cdns['local']

        self.register_controllers()
        self.register_objects()

    def register_controllers(self):
        from .portal import PortalController
        PortalController(self)

    def register_objects(self):
        self.add_template_global(enumerate)
        self.add_template_global(len)


db = SQLAlchemy()
bootstrap = Bootstrap()
app = Application()
migrate = Migrate(app, db)
