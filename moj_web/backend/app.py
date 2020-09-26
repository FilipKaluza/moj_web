from flask import Flask, render_template
from .models import db

import os

## import Blueprints
from .aboutme.controller import about
from .admin.controller import admin
from .contact.controller import contact
from .games.controller import games
from .home.controller import home

flask_app = Flask(__name__, template_folder="../frontend/templates") ##template folder preto, že mám backend v inom priečinku

flask_app.config.from_pyfile("/vagrant/configs/development.py")

db.init_app(flask_app)

## registrácia Blueprintov
flask_app.register_blueprint(about)
flask_app.register_blueprint(admin)
flask_app.register_blueprint(contact)
flask_app.register_blueprint(games)
flask_app.register_blueprint(home)


## ERROR handler
@flask_app.errorhandler(500)
def Internal_server_error(error):
    return render_template("errors/500.jinja"), 500

@flask_app.errorhandler(404)
def Internal_server_error(error):
    return render_template("/errors/404.jinja"), 404

## CLI COMMAND
def init_db(app):
        with app.app_context():
            db.create_all()
            print("Database inicialized")

            default_user = User(username="admin")
            default_user.set_password("admin")
            db.session.add(default_user)
            db.session.commit()
            print("default user was created")
