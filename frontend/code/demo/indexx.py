from flask import Flask, render_template, request
import pyarrow as pa
import redis
import pandas as pd
app = Flask(__name__)
import pyarrow as pa
import redis
import pandas as pd
@app.route('/',methods=['Get'])
def index():
   return render_template('index.html')

@app.route('/hello',methods=['Get'])
def hello_world():
   return 'hello world'

@app.route('/result',methods = ['POST', 'GET'])
def result():
   #if request.method == 'POST':
   if True:
      #result = request.form
      movie = pd.read_csv('movies.csv')

      m = movie.set_index("movieId")
      input_ = request.form.to_dict()
      movie_ID = input_['電影名字']
      input_s = int(movie_ID)
      m  = movie.iloc[input_s]
      select = pd.Series(m, index = m.keys())
      a = select[2]
      b = a.split("|")
      #c = b[1]
      ans = set(b)


      #result = request.form.to_dict()
      #result = list(result.values())[0]
      return render_template("index.html",result = ans)
      #return render_template("result.html",result = ans)
      

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)