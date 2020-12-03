import pyarrow as pa
import redis
import pandas as pd

# 宣告 redis 連線
r = redis.Redis(host='master.tibame', port=6379, db=0)
context = pa.default_serialization_context()

# 從 redis 讀取 recomm 資料
data = r.get('recomm')

# 反序列化
df = pd.DataFrame.from_dict(context.deserialize(data))

print(df.head())