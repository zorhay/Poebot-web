from flask import Flask
from .config import BaseConfig
from .extensions import login_manager, db, migrate
from .utils import get_current_time
from .constants import AnonymousUser


def create_app():
    app = Flask(BaseConfig.PROJECT)
    configure_extensions(app)
    configure_blueprint(app)
    configure_template_filters(app)
    app.config.from_object(BaseConfig)

    return app


def configure_blueprint(app):
    from .admin import admin
    admin.init_app(app)


def configure_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db=db)

    from .admin.models import AdminUser

    login_manager.anonymous_user = AnonymousUser

    @login_manager.user_loader
    def load_user(token):
        return AdminUser.get_by_id(token)

    login_manager.setup_app(app)


def configure_template_filters(app):
    """Configure filters."""

    app.jinja_env.globals['now'] = get_current_time()
