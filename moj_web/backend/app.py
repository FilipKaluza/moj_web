from flask import Flask, render_template, request
from .models import db
from flask_mail import Mail, Message
from .contactform import contactForm
import smtplib

import os

## import Blueprints
from .aboutme.controller import about
from .admin.controller import admin
from .games.controller import games
from .home.controller import home

flask_app = Flask(__name__, template_folder="../frontend/templates") ##template folder preto, že mám backend v inom priečinku

flask_app.config.from_pyfile("/vagrant/configs/development.py")
flask_app.config['RECAPTCHA_USE_SSL'] = False
flask_app.config['RECAPTCHA_PUBLIC_KEY'] = "6LfLQNMZAAAAAN5I6ODbPF2TowIUW0vgN5U8fyKF"
flask_app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
flask_app.config['MAIL_SERVER']='smtp.gmail.com'
flask_app.config['MAIL_PORT'] = 465
flask_app.config['MAIL_USERNAME'] = os.environ.get("MOJ_WEB_EMAIL_USERNAME", None)
flask_app.config['MAIL_PASSWORD'] = os.environ.get("MOJ_WEB_EMAIL_PASSWORD", None)
flask_app.config['MAIL_USE_TLS'] = False
flask_app.config['MAIL_USE_SSL'] = True
mail = Mail(flask_app)


db.init_app(flask_app)

## registrácia Blueprintov
flask_app.register_blueprint(about)
flask_app.register_blueprint(admin)

flask_app.register_blueprint(games)
flask_app.register_blueprint(home)


## ERROR handler
@flask_app.errorhandler(500)
def Internal_server_error(error):
    return render_template("errors/500.jinja"), 500

@flask_app.errorhandler(404)
def Internal_server_error(error):
    return render_template("/errors/404.jinja"), 404


@flask_app.route('/contact/', methods=["GET", "POST"])
def view_contact():
    contactform = contactForm()
    if request.method == 'POST' and contactform.validate_on_submit():
        msg = Message(contactform.name.data, sender=contactform.email.data, recipients=['kaluzafilip33@gmail.com'])
        msg.body = """
        From: %s &lt;%s&gt;
        %s
        """ % (contactform.name.data, contactform.email.data, contactform.text.data)
        mail.send(msg)
        return render_template('contact/contact.jinja', contactform=contactform)
    
    else:
        return render_template('contact/contact.jinja', contactform=contactform)

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
