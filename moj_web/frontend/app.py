from flask import Flask, url_for

from flask import Flask, render_template, request
from flask import g
from flask import redirect ##pre adminpage login
from flask import url_for ##pre adminpage
from flask import session ## umožnuje prácu s cookies pre indentifikáciu usera
from flask import flash ##flash správy

## pre DB
from .models import db
from .models import Quote #import tab Quote
from .models import User

## FORMS
from .forms import QuoteForm, loginForm, changePasswordForm

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

##for @login_required 
from functools import wraps
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "logged" not in session:
            flash("You must be logged in", "alert-danger")
            return redirect(url_for("view_login"))
        return func(*args, **kwargs)
    return decorated_function

## Adminpage
@flask_app.route('/admin/')
@login_required
def view_adminpage():
    page = request.args.get("page", 1, type=int)
    paginate = Quote.query.order_by(Quote.id.desc()).paginate(page, 2, False)
    return render_template("/admin/adminpage.jinja",
    quotes=paginate.items, ##pre zobrazenie článkov
    paginate=paginate) ## potrebné pre zobrazenie číslovania)


@flask_app.route('/admin/quotes/new/', methods=["GET"])
@login_required
def view_add_quote():
    form = QuoteForm()
    return render_template("/admin/quote_editor.jinja", form=form)


## s metódou POST na pridanie citátu
@flask_app.route('/admin/quotes/', methods=["POST"])
@login_required
def add_quote():
    add_form = QuoteForm(request.form)
    if add_form.validate():
        new_quote = Quote(
            author = add_form.author.data,
            content = add_form.content.data,
            html_render = add_form.html_render.data)
        db.session.add(new_quote)
        db.session.commit()
        flash(u"Quote was added", category="alert-success")
        return redirect(url_for("view_adminpage"))

## editácia citátu
@flask_app.route('/admin/quotes/<int:quote_id>/edit/', methods=["GET"])
@login_required
def view_quote_editor(quote_id):
    quote = Quote.query.filter_by(id = quote_id).first()
    if quote:
        form = QuoteForm()
        form.author.data = quote.author
        form.content.data = quote.content
        return render_template("/admin/quote_editor.jinja", quote = quote, form=form)
    return render_template("quote_not_found.jinja", quote_id = quote_id)


@flask_app.route('/admin/quotes/<int:quote_id>/', methods=["POST"])
@login_required
def edit_quote(quote_id):
    quote = Quote.query.filter_by(id = quote_id).first()
    if quote:
        edit_form = QuoteForm(request.form)
        if edit_form.validate():
            quote.author = edit_form.author.data
            quote.content = edit_form.content.data
            print(edit_form.author.data)
            quote.html_render = edit_form.html_render.data
            db.session.add(quote)
            db.session.commit()
            flash("Changes was saved", "success")
            return redirect(url_for("view_adminpage", quote_id = quote_id))


## CHANGE PASSWORD
@flask_app.route("/admin/changepassword/", methods=["GET"])
@login_required
def view_change_password():
    form = changePasswordForm()
    return render_template("admin/change_password.jinja", form=form)

@flask_app.route("/admin/changepassword/", methods=["POST"])
@login_required
def change_password():
    form = changePasswordForm(request.form)
    if form.validate():
        user = User.query.filter_by(username = session["logged"]).first()
        if user and user.check_password(form.old_password.data):
            user.set_password(form.new_password.data)
            db.session.add(user)
            db.session.commit()
            flash("Password was changed", category="success")
            return redirect(url_for("view_adminpage"))
        else:
            flash(" Incorrect password, try again", "danger")
            return redirect(url_for("view_login"))

##LOG IN
@flask_app.route('/admin/login/', methods=["GET"])
def view_login():
    login_form = loginForm()
    return render_template("/admin/login.jinja", form=login_form)

@flask_app.route('/admin/login/', methods=["POST"])
def login_user():
    login_form = loginForm(request.form) ## inštancia formuláru loginForm
    if login_form.validate(): ##ak sú obe polia vyplnené
        user = User.query.filter_by(username = login_form.username.data).first()
        if user and user.check_password(login_form.password.data):
            session["logged"] = user.username
            flash("Login succesfull", category="success")
            return redirect(url_for("view_adminpage"))
        else:
            flash("Invalid username or password", category="danger")
            return redirect(url_for("view_login"))
    else:
        for error in login_form.errors:
            flash("{} is missing".format(error), "danger")
        return redirect(url_for("view_login"))


##LOGOUT
@flask_app.route('/admin/logout/', methods=["POST"])
def logout_user():
    session.pop("logged")
    flash(u"You had been logged out", category="success")
    return redirect(url_for("view_homepage"))




## ERROR handler
@flask_app.errorhandler(500)
def Internal_server_error(error):
    return render_template("500.jinja"), 500

@flask_app.errorhandler(404)
def Internal_server_error(error):
    return render_template("404.jinja"), 404



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
