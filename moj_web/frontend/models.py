from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.String)
    content = db.Column(db.Integer, unique = True)