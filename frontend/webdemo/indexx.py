from flask import Flask, render_template, request
from IMDBaver import runPy
from counIMDB import runcoun
from joblib import load
import pandas as pd
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from sklearn.metrics import plot_confusion_matrix
import redis
import pymysql
import re
import pyarrow as pa

app = Flask(__name__)

@app.route('/',methods=['Get', 'POST'])
def index():
   return render_template('index.html')

@app.route('/predict',methods=['Get', 'POST'])
def predict():
   model = load('/Users/goldenman/Desktop/webdemo/Prediction_Model/Model/Logistic_Regression.joblib') 
   df = pd.read_csv('/Users/goldenman/Desktop/webdemo/Prediction_Model//2020_series_tmp.csv')

   #載入2020年資料
   X = df.drop(['Title','Won'],axis=1)
   y = df['Won']

   # 特徵縮放
   scaler = preprocessing.StandardScaler().fit(X)

   #標準化 X
   X_nor = scaler.transform(X)

   #用以訓練好的模型進行預測
   y_pred = model.predict(X_nor)

   result = y_pred.tolist() #numpy array to list

   index_list = []

   for index,value in enumerate(result):
      if value == 1:
         index_list.append(index)

   print("The prediction of  the Primetime Emmy's Award in 2020：")
   #列出預測的得獎影集
   res = []
   for i in index_list:
    re = df.at[i,'Title']
    res.append(re)

   return render_template('index.html',result1=res)

@app.route('/chart',methods=['GET', 'POST'])
def chart():
   return render_template('chart.html')

@app.route('/chart123',methods=['GET', 'POST'])
def chart1():
   if request.method == 'GET':
      print("OK")
      runPy()
      return render_template('chart.html')
   else:
      return render_template('chart.html')

@app.route('/chart122',methods=['GET', 'POST'])
def chart2():
   if request.method == 'GET':
      print("OK")
      runcoun()
      return render_template('chart.html')
   else:
      return render_template('chart.html')


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)