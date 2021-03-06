from flask import Flask, render_template, request
import pyarrow as pa
import redis
import pandas as pd
app = Flask(__name__)

import pymysql
import re


r = redis.Redis(host='10.2.1.234', port=6379, db=0)
context = pa.default_serialization_context()

# 從 redis 讀取 recomm 資料
data = r.get('recomm')

# 反序列化
df = pd.DataFrame.from_dict(context.deserialize(data))




@app.route('/',methods=['Get'])
def index():
   return render_template('index.html')

@app.route('/hello',methods=['Get'])
def hello_world():
   return 'hello world'

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':

        
    #連接movie資料庫
        movie = pd.read_csv('movies.csv')

    #接收movieId
        input_ = request.form.to_dict()
        movie_ID = input_['電影名字']
        input_s = int(movie_ID)

    #movieId帶進模型運算
        m  = movie.iloc[input_s]
        select = pd.Series(m, index = m.keys())

    #取出結果
        #a = 選取user的電影類型
        a = select[2]
        #c =split結果變list
        c = a.split("|")
        
        b = []
        user1 = [] 
        for item in c:
            category = ['Horror','Children','Comedy','Adventure', 'Fantasy', 'Animation', 'Musical','Action', 'Crime', 'Thriller','Romance', 'Documentary', 'War', 'Drama', 'Mystery']
            for i in category:
                pattern =  r'.*{}.*'.format(i)
                result = re.match(pattern,item)
                if result != None:
                    b.append(i)
                else:
                    pass
    
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

    return render_template("result.html",result = output)


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)
        