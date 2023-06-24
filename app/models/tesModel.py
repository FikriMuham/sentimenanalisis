from app import db

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
# from datetime import datetime
# from sqlalchemy import func
# from flask_sqlalchemy import SQLAlchemy

class TesModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # tanggal = db.Column(db.DateTime, default=datetime.utcnow, onupdate=func.now())
    Tweet = db.Column(db.Text)
    label = db.Column(db.String(100))

    def __init__(self, Tweet, label):
        # self.tanggal = tanggal
        self.Tweet = Tweet
        self.label = label

class TesModelForm(FlaskForm):
    # tanggal = StringField('Tanggal', validators=[DataRequired()])
    label = StringField('Label', validators=[DataRequired()])
    Tweet = StringField('Tweet', validators=[DataRequired()])
    submit = SubmitField('Simpan')

