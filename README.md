# 成衣生產效率診斷與瓶頸分析 （Garment Production Efficiency Diagnosis & Bottleneck Analysis）
利用 SQL 與 Python 實現數據驅動決策

### 業務問題 (Business Problem)
- 痛點：工廠每日產生大量數據，但管理層難以快速識別哪些生產線（Team）處於亞健康狀態。
- 目標：建立自動化監控機制，找出「效率缺口（Efficiency Gap）」並量化影響因子（如閒置人力、加班、款式變更）。


### 技術亮點 (Technical Highlights)
- SQL 資料清洗：強調處理日期格式不一、時間維度聚合（Week-level）的能力。
- 熱力圖 (Heatmap) 矩陣：強調視覺心理學應用，利用 RdYlGn 配色讓管理層在 3 秒內鎖定負值區域。
- 統計驗證 (Regression Analysis)：不只是看圖說故事，而是透過 $p$-value 與係數證明 idle_men 與 department_sewing 是導致效率滑坡的主因。

  
### 關鍵洞察與行動建議 (Insights & Action)
- 異常診斷：Team 10 在 Week：201508 的暴跌可能與兩筆資料中皆有Idle_men激增至35人有關，詳細內容可能還需要去現場了解狀況。
- 全廠趨勢：第 8、9 週的集體下滑與Idle Men 閒置工人發生的事件約有2/3發生在該週呈高度相關。
- 標竿學習：Team 1, 3 長期保持正向缺口，具備 SOP 複製價值。
