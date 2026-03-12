import pandas as pd
from sqlalchemy import create_engine
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import gridspec


# 1. 設定資料庫連線資訊 
# 格式: mysql+pymysql://帳號:密碼@主機位址:連接埠/資料庫名稱
user = 'root'
password = 'young0960102123'
host = 'localhost'
port = '3306'
db_name = 'testdb'

engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}')

# 2. SQL 語法
sql_query = """
SELECT 
    `team`, 
    YEARWEEK(STR_TO_DATE(`date`, '%%Y-%%m-%%d'), 1) AS `work_week`, 
    ROUND(AVG(`actual_productivity` - `targeted_productivity`), 6) AS `avg_gap`
FROM `garment`
GROUP BY `team`, `work_week`
ORDER BY `work_week`, `team`;
"""

# 1. 執行 SQL 並取得 df...
df = pd.read_sql(sql_query, engine)

# 2. 建立週別矩陣 (原始順序)
heatmap_data = df.pivot(index='team', columns='work_week', values='avg_gap')

# A. 先算總平均
team_overall_avg = heatmap_data.mean(axis=1).to_frame(name='Total Avg')

# B. 取得「從高到低」的索引順序 (ascending=False 代表由大到小)
sort_index = team_overall_avg.sort_values('Total Avg', ascending=False).index

# C. 根據這個順序重新排列兩份資料
heatmap_data = heatmap_data.reindex(sort_index)
team_overall_avg = team_overall_avg.reindex(sort_index)

# 3. 設定畫布
fig = plt.figure(figsize=(15, 8))
gs = gridspec.GridSpec(1, 2, width_ratios=[15, 1], wspace=0.05) 

ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

# 4. 畫主圖
sns.heatmap(heatmap_data, cmap='RdYlGn', center=0, annot=True, fmt=".3f", 
            ax=ax1, cbar=False)
ax1.set_title('Sorted Weekly Team Efficiency Gap')

# 5. 畫平均邊欄
sns.heatmap(team_overall_avg, cmap='RdYlGn', center=0, annot=True, fmt=".3f", 
            ax=ax2, cbar=True, yticklabels=False)
ax2.set_title('Avg')

plt.show()



# ------------------------- productivity trend ------------------
