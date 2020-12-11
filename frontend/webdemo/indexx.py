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

@app.route('/result',methods = ['POST', 'GET'])
def result():
   r = redis.Redis(host='10.2.1.234', port=6379, db=0)
   context = pa.default_serialization_context()
   data = r.get('recomm')
   df = pd.DataFrame.from_dict(context.deserialize(data))
   movie = pd.read_csv('/Users/goldenman/Desktop/clubs-5 web/webapp/frontend/code/demo/movies.csv')
   if request.method == 'POST':    
      #input_ = request.form.to_dict()    
      #輸入userid
      uId = request.form.get('電影名字')
      uId = int(uId)
      recom_movieId = df[df['userId'] == uId]['movieId'].to_list()
      recom_movieId = recom_movieId[0]
      #print(recom_movieId)
      b = []
      for movieId in recom_movieId:
         #print(movieId)
         movieId_2 = movieId
         results = movie[movie['movieId'] == movieId_2]['genres'].apply(lambda x:  x.split('|')).to_list()
         #usertype
         c = results[0]
         
         #建立類型做正則表示
         for item in c:
            category = ['Horror','Children','Comedy','Adventure', 'Fantasy', 'Animation', 'Musical','Action', 'Crime', 'Thriller','Romance', 'Documentary', 'War', 'Drama', 'Mystery']
            for i in category:
               pattern =  r'.*{}.*'.format(i)
               result = re.match(pattern,item)
               if result != None:
                  b.append(i)
               else:
                  pass    
      #db = pymysql.connect(host="18.183.130.58", user="root", passwd="tibame", db="TVShows")
      db = pymysql.connect(host="10.2.1.234", user="root", passwd="tibame", db="TVShows")
      cursor = db.cursor()
      cursor.execute("SELECT Title, Year_x, imdbRating, Genre FROM imdbdata order by imdbRating DESC, Year_x DESC ")
      result = cursor.fetchall()
      count = 0
      ans = []
      for record in result:
         col1 = record[0]
         col2 = record[1]
         col3 = record[2]
         col4 = record[3]
         col4 = col4.split("|")  
         for genre in col4:
            if count >  4:
               break
            for custype in b:
               if genre == custype:
                  ans.append(col1)
                  count += 1
               else:
                  pass
                   
   output = {
   "1":ans[0],
   "2":ans[1],
   "3":ans[2],
   "4":ans[3],
   "5":ans[4]
   }

   Table = []
   for key, value in output.items():
      temp = []
      temp.extend([key,value])
      Table.append(temp)

   return render_template("index.html",result = Table)

if __name__ == "__main__":
   app.run(debug=True, host='localhost', port=5000)