from flask import Flask, render_template, request
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.ml.feature import VectorAssembler,VectorIndexer,OneHotEncoder,StringIndexer
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator




app = Flask(__name__)
#@app.route('/')
#def student():
 #  return render_template('student.html')

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/predict',methods=['POST', 'GET'])
def predict():
    if True:
        result = request.form
        return render_template("result.html",result = result)

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if True:
      result = request.form
      return render_template("result.html",result = result)



#@app.route('/result',methods = ['POST', 'GET'])
#def result():
#   if request.method == 'POST':
 #  if True:
  #    result = request.form
   #   return render_template("result.html",result = result)


if __name__ == '__main__':
   app.run(debug = True)




