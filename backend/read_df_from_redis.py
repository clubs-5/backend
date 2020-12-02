import pyarrow as pa
import redis

# 宣告 redis 連線
r = redis.Redis(host='master.tibame', port=6379, db=0)

# 從 redis 讀取 recomm 資料
data = r.get('recomm')

# 反序列化

df = pa.deserialize(data)

