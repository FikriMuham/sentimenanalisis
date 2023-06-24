import os
from flask import Flask, request, flash, render_template, jsonify, json
from app.controllers.function import preprocess_data, result_svm
import pandas
from app import db


labels = [
  'POSITIF', 'NEGATIF', 'NETRAL'
]

colors = [
  '#1cc88a', '#e74a3b', '#f6c23e'
]

def klasifikasi():
    # text = pandas.read_csv('app/uploads/datauji.csv', encoding='latin-1')
    text = db.session.execute("SELECT Tweet, label FROM hasil_sentimen")
    tableData = pandas.DataFrame(text, columns=['Tweet', 'label'])
    tableData['label'] = tableData['label']

    accuracy_rbf, y_test = result_svm(tableData)
    accuracy_rbf = (round(accuracy_rbf, 3) * 100)
    
    y_test = y_test.reset_index()
    netral, negatif, positif = y_test['label'].value_counts()
    total = positif + negatif + netral
    # print(y_test['label'].value_counts() )

    pie_labels = labels
    pie_colors = colors
    pie_values = [positif, negatif, netral]

    bar_labels = labels
    bar_values = [positif, negatif, netral]

    # tableData = pandas.read_csv('app/uploads/datauji.csv', usecols=['Text','label'],encoding='latin-1' )
    # tableData['label'] = tableData['label']
    
    return render_template ('klasifikasinv.html', tweet_positive = positif, tweet_negative = negatif, tweet_netral = netral, total_tweet = total, accuracy_rbf = accuracy_rbf, labels = pie_labels, colors = pie_colors, values = pie_values, bar_labels = bar_labels, bar_values = bar_values, tables=[tableData.to_html(classes='table table-bordered', table_id='dataTable')])