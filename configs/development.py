import os

DEBUG = True
#DATABASE = "/vagrant/blog.db"
SQLALCHEMY_DATABASE_URI = "sqlite:////vagrant/quotes.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get("MOJ_WEB_SECRET_KEY", None)



