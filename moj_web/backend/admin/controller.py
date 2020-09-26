from flask import Blueprint, url_for, render_template, request
from flask import redirect ##pre adminpage login
from flask import url_for ##pre adminpage
from flask import session ## umožnuje prácu s cookies pre indentifikáciu usera
from flask import flash ##flash správy

## pre DB
from moj_web.backend.models import db
from moj_web.backend.models  import Quote #import tab Quote
from moj_web.backend.models  import User

## FORMS
from .forms import QuoteForm, loginForm, changePasswordForm

admin= Blueprint("admin", __name__)

##for @login_required 
from functools import wraps
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "logged" not in session:
            flash("You must be logged in", "alert-danger")
            return redirect(url_for("admin.view_login"))
        return func(*args, **kwargs)
    return decorated_function

## Adminpage
@admin.route('/admin/')
@login_required
def view_adminpage():
    page = request.args.get("page", 1, type=int)
    paginate = Quote.query.order_by(Quote.id.desc()).paginate(page, 2, False)
    return render_template("/admin/adminpage.jinja",
    quotes=paginate.items, ##pre zobrazenie článkov
    paginate=paginate) ## potrebné pre zobrazenie číslovania)


@admin.route('/admin/quotes/new/', methods=["GET"])
@login_required
def view_add_quote():
    form = QuoteForm()
    return render_template("/admin/quote_editor.jinja", form=form)


## s metódou POST na pridanie citátu
@admin.route('/admin/quotes/', methods=["POST"])
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
        return redirect(url_for("admin.view_adminpage"))

## editácia citátu
@admin.route('/admin/quotes/<int:quote_id>/edit/', methods=["GET", "DELETE"])
@login_required
def view_quote_editor(quote_id):
    quote = Quote.query.filter_by(id = quote_id).first()
    if quote:
        form = QuoteForm()
        form.author.data = quote.author
        form.content.data = quote.content
        return render_template("/admin/quote_editor.jinja", quote = quote, form=form)
    return render_template("/admin/quote_not_found.jinja", quote_id = quote_id)


@admin.route('/admin/quotes/<int:quote_id>/', methods=["POST"])
@login_required
def edit_quote(quote_id):
    quote = Quote.query.filter_by(id = quote_id).first()
    if quote:
        edit_form = QuoteForm(request.form)
        if edit_form.validate():
            quote.author = edit_form.author.data
            quote.content = edit_form.content.data
            quote.html_render = edit_form.html_render.data
            db.session.add(quote)
            db.session.commit()
            flash("Changes was saved", "success")
            return redirect(url_for("admin.view_adminpage", quote_id = quote_id))

## s metódou DELETE na ostránenie citátu
@admin.route("/admin/quotes/delete/<int:quote_id>/", methods=["GET"])
@login_required
def remove_quote(quote_id):
    quote = Quote.query.filter_by(id = quote_id).first()
    if quote:
        db.session.delete(quote)
        db.session.commit()
        flash("Quote was removed", "success")
        return redirect(url_for("admin.view_adminpage"))


## CHANGE PASSWORD
@admin.route("/admin/changepassword/", methods=["GET"])
@login_required
def view_change_password():
    form = changePasswordForm()
    return render_template("/admin/change_password.jinja", form=form)

@admin.route("/admin/changepassword/", methods=["POST"])
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
            return redirect(url_for("admin.view_adminpage"))
        else:
            flash(" Incorrect password, try again", "danger")
            return redirect(url_for("admin.view_login"))

##LOG IN
@admin.route('/admin/login/', methods=["GET"])
def view_login():
    login_form = loginForm()
    return render_template("/admin/login.jinja", form=login_form)

@admin.route('/admin/login/', methods=["POST"])
def login_user():
    login_form = loginForm(request.form) ## inštancia formuláru loginForm
    if login_form.validate(): ##ak sú obe polia vyplnené
        user = User.query.filter_by(username = login_form.username.data).first()
        if user and user.check_password(login_form.password.data):
            session["logged"] = user.username
            flash("Login succesfull", category="success")
            return redirect(url_for("admin.view_adminpage"))
        else:
            flash("Invalid username or password", category="danger")
            return redirect(url_for("admin.view_login"))
    else:
        for error in login_form.errors:
            flash("{} is missing".format(error), "danger")
        return redirect(url_for("admin.view_login"))


##LOGOUT
@admin.route('/admin/logout/', methods=["GET", "POST"])
@login_required
def logout_user():
    session.pop("logged")
    flash(u"You had been logged out", category="success")
    return redirect(url_for("home.view_homepage"))


