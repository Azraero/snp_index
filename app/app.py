from flask import Flask, render_template
from settings import config
from .exetensions import Mail

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    register_blueprint(app)
    register_exetensions(app)
    register_errorhandlers(app)
    return app


def register_blueprint(app):
    from .main import main as main_blueprint
    from .tools import tools as tools_blueprint
    from .expr import expr as expr_blueprint
    from .snp import snp as snp_blueprint
    from .auth import auth as auth_blueprint
    from .variation import variation as variation_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(variation_blueprint)
    app.register_blueprint(tools_blueprint)
    app.register_blueprint(expr_blueprint)
    app.register_blueprint(snp_blueprint)
    app.register_blueprint(auth_blueprint)
    return None


def register_exetensions(app):
    Mail.init_app(app)
    return None


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
