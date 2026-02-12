from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    google_drive_id = db.Column(db.String(255))
    folder_id = db.Column(db.String(255))   # NEW COLUMN
    size = db.Column(db.Integer)
    mime_type = db.Column(db.String(100))
    storage_path = db.Column(db.String(500))


