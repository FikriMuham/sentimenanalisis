from app import app
from flask import request, jsonify, render_template, redirect
from flask_marshmallow import Marshmallow
from app.models.tesModel import db, TesModel
from app.controllers.function import preprocess_data
import pickle

ma = Marshmallow(app)


class TesModelSchema(ma.Schema):
    class Meta:
        fields = ('id', 'Tweet', 'label')

# init schema
tesModel_schema = TesModelSchema()
tesModels_schema = TesModelSchema(many=True)


def addTesModel():
    tweet = request.form['Tweet']
    label = request.form['label']

    newTesModel = TesModel(tweet, label)
    db.session.add(newTesModel)
    db.session.commit()
    tesModel = tesModel_schema.dump(newTesModel)
    return jsonify({"msg": "Success add data", "status": 200, "data": tesModel})

def getAllTesModel():
    allTesModel = TesModel.query.order_by(TesModel.id.desc()).all()
    # result = tesModels_schema.dump(allTesModel)
    # result.reverse()
    allTesModel.reverse()
    return jsonify({"msg": "Success Get all data", "status": 200, "data": allTesModel})

def tesmodel():
  # Loading model to compare the results
  model = pickle.load(open('app/uploads/rbf.model','rb'))
  vectorizer = pickle.load(open('app/uploads/vectorizer.model','rb'))

  text = request.form['Tweet']
  original_text = request.form['Tweet']

  hasilprepro = preprocess_data(text)
  hasiltfidf = vectorizer.transform([hasilprepro])
  

  # cek prediksi dari kalimat
  svm = ''
  hasilsvm = model.predict(hasiltfidf)
  if hasilsvm == 0:
    svm = 'NETRAL'
  elif hasilsvm == 1:
    svm = 'NEGATIF'
  else:
    svm = 'POSITIF'


  newTesModel = TesModel(text, svm)
  db.session.add(newTesModel)
  db.session.commit()
  return render_template ('tesmodel.html', original_text=original_text, hasilprepro=hasilprepro, hasilsvm=svm)



def tesmodelAdmin():
  # Loading model to compare the results
  model = pickle.load(open('app/uploads/rbf.model','rb'))
  vectorizer = pickle.load(open('app/uploads/vectorizer.model','rb'))

  text = request.form['tweet']
  original_text = request.form['tweet']

  hasilprepro = preprocess_data(text)
  hasiltfidf = vectorizer.transform([hasilprepro])
  

  # cek prediksi dari kalimat
  svm = ''
  hasilsvm = model.predict(hasiltfidf)
  if hasilsvm == 0:
    svm = 'NETRAL'
  elif hasilsvm == 1:
    svm = 'NEGATIF'
  else:
    svm = 'POSITIF'


  newTesModel = TesModel(text, svm)
  db.session.add(newTesModel)
  tesModel = TesModel.query.all()
  table = tesModels_schema.dump(tesModel)
  db.session.commit()
  return render_template ('tesmodelAdmin.html', original_text=original_text, hasilprepro=hasilprepro, hasilsvm=svm, tables=table)

def getTesModelAdmin():
   tesModel = TesModel.query.all()
   table = tesModels_schema.dump(tesModel)
   return render_template('tesModelAdmin.html', tables=table)

