from app import app
from flask import request, jsonify, render_template, redirect
from flask_marshmallow import Marshmallow
from app.models.tesModel import db, TesModel
from app import db

ma = Marshmallow(app)

def gabung_tabel():
    data = db.session.query(hasil_sentimen, tes_model).join(tes_model, hasil_sentimen.id == tes_model.id).all()
    return render_template('tesModelAdmin.html', data=data)
