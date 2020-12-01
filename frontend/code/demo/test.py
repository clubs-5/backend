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

@app.route('/predict',methods=['POST'])
def predict():
          spark = SparkSession \
        .builder \
        .getOrCreate()

    # Prepare data
   final_data = spark.read.csv("hdfs://master.tibame/user/clubs/ml-25m/ratings.csv",
                                inferSchema=True,
                                header=True)

    # (Split data into train and test sets
    #train_data, test_data = final_data.randomSplit([0.8,0.2])
    
    # (Model training
    #als = ALS(maxIter=5,userCol="userId",itemCol="movieId",ratingCol="rating" , coldStartStrategy="drop")
    #model = als.fit(train_data)
    
    # (Transform the test data using the model to get predictions
    #model.write().overwrite().save("hdfs://master.tibame/user/clubs/spark_mllib_101/movies/movies_recommender/")


    # (Specify the number of movies you would like to recommand for each user
    #user_movies = model.recommendForAllUsers(5)

    # (user_movies.show(100, truncate=False)
    #result = user_movies.filter(user_movies.userId == 544).collect()
 


       if True:
  

            
          userId = request.form['userId']
          movieId = request.form['movieId']
          rating = request.form['rating']
          timestamp = request.form['timestamp']
          data = [userId, movieId, rating, timestamp]
          columns = ['userId', 'movieId', 'rating', 'timestamp']
          newuser = [(userId, movieId, rating, timestamp)]
          newrow = spark.createDataFrame(newuser, columns)
          appended = final_data.union(newrow)
          train_data, test_data = final_data.randomSplit([0.8,0.2])
          
          #訓練模習
          als = ALS(maxIter=5,userCol="userId",itemCol="movieId",ratingCol="rating" , coldStartStrategy="drop")
          #新模型
         model = als.fit(train_data)
         #寫回舊模型
         model.write().overwrite().save("hdfs://master.tibame/user/clubs/spark_mllib_101/movies/movies_recommender/")

         user_movies = model.recommendForAllUsers(5)
         result = user_movies.filter(user_movies.userId == userId).collect()

          return render_template("result.html",result = result)
      
      
      




#@app.route('/result',methods = ['POST', 'GET'])
#def result():
#   if request.method == 'POST':
 #  if True:
  #    result = request.form
   #   return render_template("result.html",result = result)


if __name__ == '__main__':
   app.run(debug = True)






