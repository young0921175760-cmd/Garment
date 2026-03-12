# ------------------------- productivity trend ------------------

import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import seaborn as sns
from matplotlib import gridspec

# 1. 設定資料庫連線資訊 (請根據你的設定修改)
# 格式: mysql+pymysql://帳號:密碼@主機位址:連接埠/資料庫名稱
user = 'root'
password = 'young0960102123'
host = 'localhost'
port = '3306'
db_name = 'testdb'

engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}')

# 2. 放入你剛剛寫好的 SQL 語法
sql_query = """
SELECT 
    YEARWEEK(STR_TO_DATE(`date`, '%%Y-%%m-%%d'), 1) AS `work_week`,
    ROUND(AVG(`efficiency_gap`), 3) AS `avg_gap` 
FROM `garment`
GROUP BY `work_week`
ORDER BY `work_week`;
"""

# 1. 假設 df 是你從 SQL 讀入的資料
df = pd.read_sql(sql_query, engine)


# 1. 假設 df 是你從 SQL 讀入的資料，且欄位名為 work_week
# 這裡我們手動處理格式轉換
df['display_week'] = df['work_week'].astype(str).apply(lambda x: f"{x[:4]}/{int(x[4:])}")

# 2. 設定顏色（沿用之前的邏輯）
colors = ['#228B22' if x >= 0 else '#FF6347' for x in df['avg_gap']]

# 3. 開始繪圖
plt.figure(figsize=(12, 6))
bars = plt.bar(df['display_week'], df['avg_gap'], color=colors, edgecolor='black', alpha=0.8)

# 4. 畫出 0 基準線
plt.axhline(0, color='black', linewidth=1.5)

# 5. 在長條圖上方/下方標註數值w
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, 
             f"{yval:.3f}", 
             va='bottom' if yval > 0 else 'top', 
             ha='center', fontsize=10, fontweight='bold')

# 6. 圖表美化
plt.title('Weekly Factory Efficiency Gap (Formatted)', fontsize=14, pad=20)
plt.xlabel('Year/Week', fontsize=12)
plt.ylabel('Average Efficiency Gap', fontsize=12)

# 如果週數很多，可以旋轉標籤避免重疊
plt.xticks(rotation=45) 
plt.grid(axis='y', linestyle='--', alpha=0.4)

plt.tight_layout()
plt.show()