from flask import Blueprint, render_template

contact = Blueprint("contact", __name__)

@contact.route('/contact/')
def view_contact():
    return render_template("contact/contact.jinja")