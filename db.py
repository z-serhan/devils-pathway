from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Major(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique=False, nullable=False)
