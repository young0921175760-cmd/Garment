#regression_garments
import pandas as pd
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
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
SELECT *
FROM `garment`

"""
# 1. 執行 SQL 
df = pd.read_sql(sql_query, engine)


# 清除所有字串欄位的前後空格
df['department'] = df['department'].str.strip()
print(df['department'].unique())

# 處理缺失值 
df['wip'] = df['wip'].fillna(0)
df['wip_load'] = df['wip_load'].fillna(0)

# 3. 類別變數處理 (例如 department: sewing=1, finishing=0)
df = pd.get_dummies(df, columns=['department'], drop_first=True)

# 4. 設定自變數 (X) 與 因變數 (y)
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

# 3. 將整個 DataFrame 轉換為 float64 
X = X.astype(float)
y = y.astype(float)

# 4. 加入常數項
X = sm.add_constant(X)

model = sm.OLS(y, X).fit()
print(model.summary())


# ---------------------- 圖表設定 -------------------------------------------

plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (10, 6)

import matplotlib.pyplot as plt
import pandas as pd

def plot_coefficients_clean_labeled(model):
    # 提取數據
    params = model.params.drop('const')
    conf_int = model.conf_int().drop('const')
    
    coef_df = pd.DataFrame({
        'Feature': params.index,
        'Coef': params.values,
        'Error': params.values - conf_int[0]
    }).sort_values(by='Coef', ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 繪製誤差棒圖
    eb = ax.errorbar(coef_df['Coef'], coef_df['Feature'], xerr=coef_df['Error'], 
                     fmt='o', color='royalblue', capsize=5, markersize=8)
    
   
    for i, row in enumerate(coef_df.itertuples()):
        if row.Feature == 'department_sewing':
            # 將數值放正下方 (va='top', y偏移量為負)
            ax.annotate(f'{row.Coef:.4f}', 
                        xy=(row.Coef, i), 
                        xytext=(0, 15), 
                        textcoords='offset points',
                        ha='center', # 水平置中
                        va='top', # 垂直靠上
                        fontsize=11,
                        fontweight='bold',
                        color='darkblue')
        else:
            ha_pos = 'left' if row.Coef >= 0 else 'right'
            txt_offset = 12 if row.Coef >= 0 else -12
            ax.annotate(f'{row.Coef:.4f}', 
                        xy=(row.Coef, i), 
                        xytext=(txt_offset, 0), # 左右偏移像素
                        textcoords='offset points',
                        ha=ha_pos, 
                        va='center',
                        fontsize=10,
                        fontweight='bold',
                        color='darkblue')

    # 設定圖表細節
    ax.axvline(x=0, color='red', linestyle='--', linewidth=1, alpha=0.7)
    ax.set_title('Impact of Factors on Efficiency Gap (Cleaned View)', fontsize=14, pad=20)
    ax.set_xlabel('Coefficient Value', fontsize=12)
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # 找出數據的真實邊界
    x_min = coef_df['Coef'].min() - coef_df['Error'].max() - 0.02 # 左邊多留一點給裁縫部的線
    x_max = coef_df['Coef'].max() + coef_df['Error'].max() + 0.02 # 右邊只留一點點
    
    # 設定 X 軸極限
    ax.set_xlim(x_min, x_max)

    plt.tight_layout()
    plt.savefig('regression_coefficients_cleaned.png', dpi=300)
    plt.show()

plot_coefficients_clean_labeled(model)
