from flask import Blueprint, render_template
from flask import send_file ##pre PDF

about = Blueprint("about", __name__)

@about.route('/aboutme/', methods=["GET"])
def view_aboutmepage():
    return render_template("aboutme/aboutme.jinja")

@about.route('/aboutme/download')
def downloadCV():
	path = "static/cv.pdf"
	return send_file(path, as_attachment=True)
