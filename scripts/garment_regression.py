#regression_garments
import pandas as pd
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from matplotlib import gridspec



# 1. 設定資料庫連線資訊
user = 'root'
password = 'young0960102123'
host = 'localhost'
port = '3306'
db_name = 'testdb'

engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}')

# 2. SQL 語法
sql_query = """
SELECT *
FROM `garment`

"""
# 1. (前略) 執行 SQL 並取得 df...
df = pd.read_sql(sql_query, engine)

# 處理缺失值
df['wip'] = df['wip'].fillna(0)
df['wip_load'] = df['wip_load'].fillna(0)

# 3. 類別變數處理 (例如 department: sewing=1, finishing=0)
df = pd.get_dummies(df, columns=['department'], drop_first=True)

# 4. 設定自變數 (X) 與 因變數 (y)
# 這裡挑選你認為有影響的欄位
features = [
    'smv', 
    'overtime_per_worker', 
    'incentive', 
    'idle_time', 
    'idle_men', 
    'department_sewing' # 轉化後的類別變數
]

# 1. 確保所有的 X 和 y 都是數字型態，無法轉換的會變成 NaN
X = df[features].apply(pd.to_numeric, errors='coerce')
y = df['efficiency_gap'].apply(pd.to_numeric, errors='coerce')

# 2. 處理 NaN
X = X.fillna(0)
y = y.fillna(0)

# 3. 將整個 DataFrame 轉換為 float64 型態
X = X.astype(float)
y = y.astype(float)

# 4. 加入常數項
X = sm.add_constant(X)

model = sm.OLS(y, X).fit()
print(model.summary())
