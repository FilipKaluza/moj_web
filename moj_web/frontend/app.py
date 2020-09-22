from flask import Flask, url_for

from flask import Flask, render_template
from flask import g

from .models import db

flask_app = Flask(__name__)

flask_app.config.from_pyfile("/vagrant/configs/development.py")

db.init_app(flask_app)

@flask_app.route('/')
def view_homepage():
    page = request.args.get("page", 1, type=int)
    paginate = Quote.query.order_by(Quote.id.desc()).paginate(page, 2, False)
    return render_template("home/home.jinja",
    quotes=paginate.items, ##pre zobrazenie článkov
    paginate=paginate) ## potrebné pre zobrazenie číslovania)

@flask_app.route('/aboutme/')
def view_aboutmepage():
    return render_template("aboutme/aboutme.jinja")

@flask_app.route('/games/')
def view_gameslist():
    return render_template("games/games.jinja")

@flask_app.route('/games/choredoor/')
def play_choredoor():
    return render_template("games/chore_door.jinja")



@flask_app.route('/contact/')
def view_contact():
    return render_template("contact/contact.jinja")

@flask_app.route('/admin/')
def view_adminpage():
    return render_template("admin/admin.jinja")

## ERROR handler
@flask_app.errorhandler(500)
def Internal_server_error(error):
    return render_template("errors/500.jinja"), 500

@flask_app.errorhandler(404)
def Internal_server_error(error):
    return render_template("errors/404.jinja"), 404



## CLI COMMAND

def init_db(app):
        with app.app_context():
            db.create_all()
            print("Database inicialized")

