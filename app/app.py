from flask import Flask
from settings import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

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
    return app
