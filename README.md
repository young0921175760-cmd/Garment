# 成衣生產效率診斷與瓶頸分析 （Garment Production Efficiency Diagnosis & Bottleneck Analysis）

### 專案背景與業務問題 (Project Overview)
在製造管理中，單純的產出數據往往無法揭示「效率流失」的根因。本專案透過分析成衣廠 12 個團隊的生產數據，旨在解決以下核心問題：
- 識別異常：從大量數據中快速鎖定績效落後的生產線（Team）。
- 量化風險：驗證「閒置人力 (Idle Men)」與「標準 (Standard Minute Value)」對排程進度的實質影響。
- 資源優化：提供管理層預警指標，協助優化人力配置以縮減效率缺口 (Efficiency Gap)。


### 技術亮點 (Technical Workflow)
- 資料清洗 (SQL - MySQL)：
  - 處理非標準日期字串，並使用 YEARWEEK 進行時間維度聚合，以平滑單日波動。
  - 修正Department中的拼字錯誤 sweing -> sewing
  - 修正Department中因多一個空格而產生的髒資料 finishing_ -> finishing
 
- 數據分析與自動化視覺化 (Python - Pandas, Seaborn)：
  - 效率矩陣 (Heatmap)：開發自動化排序邏輯，結合視覺心理學（RdYlGn 配色）快速定位 Team 10 的極端負值區域（-0.24）。
  - 回歸統計驗證 (OLS Regression)：使用 statsmodels 進行顯著性檢定，證實 idle_men 與效率下降呈高度負相關 ($p < 0.05$)。
  - 趨勢分析：結合 Bar Chart 追蹤全廠週期性波動，發現第 8、9 週的集體效率下滑。


### 關鍵洞察與行動建議 (Insights & Action)
- 異常診斷：Team 10 在 Week：201508 的暴跌可能與兩筆資料中皆有 Idle_men 激增至35人有關，詳細內容可能還需要去現場了解狀況。
- 全廠趨勢：第 8、9 週的集體下滑與 Idle Men 閒置工人發生的事件約有 60% 發生在該週呈高度相關。
- 標竿學習：Team 1, 3 長期保持正向缺口，可能跟兩組數據中皆不存在 Idle_Men 的有關，具備 SOP 複製價值，可深入了解其運作模式。
- 排成優化：建議可以針對閒置工人的配置來建立一個模型來避開人力閒置的高峰以優化排程。
- 現場了解：針對如Team 10 第8週效率暴跌、Team 6,7,8 整體效率差距較大等，生管可介入現場相係了解產線狀況與原因並協調人力。
