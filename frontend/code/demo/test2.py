from flask import Flask, render_template, request
import pyarrow as pa
import redis
import pandas as pd
import re
import pymysql

r = redis.Redis(host='10.2.1.234', port=6379, db=0)
context = pa.default_serialization_context()

# 從 redis 讀取 recomm 資料
data = r.get('recomm')

# 反序列化
df = pd.DataFrame.from_dict(context.deserialize(data))

#從本地讀取movie資料
movie = pd.read_csv('movies.csv')

uId = 148
recom_movieId = df[df['userId'] == uId]['movieId'].to_list()
recom_movieId = recom_movieId[0]
#print(recom_movieId)
for movieId in recom_movieId:
    #print(movieId)
    movieId_2 = movieId
    results = movie[movie['movieId'] == movieId_2]['genres'].apply(lambda x:  x.split('|')).to_list()
    #usertype
    c = results[0]
    print(c)


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
print(b)

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
                #print(ans)
            else:
                pass

#for i in ans:
 #   print(i)

# print("=======")
# output = {
#     "1":ans[0],
#     "2":ans[1],
#     "3":ans[2],
#     "4":ans[3],
#     "5":ans[4]
# }
# print(output)



