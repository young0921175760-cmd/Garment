-- Setting

SHOW DATABASES;
SELECT DATABASE();
USE `Testdb`;

ALTER TABLE `Garments_all` RENAME TO `garment`;
ALTER TABLE `garment` DROP COLUMN total_work_time;

SELECT*
FROM `garment`;


-- KPI訂定: effiecency_gap, wip_load, productivity_per_worker, overtime_per_worker

ALTER TABLE `garment` ADD COLUMN efficiency_gap DECIMAL(3,2) AS (`actual_productivity`-`targeted_productivity`);	-- efficiency_gap 
ALTER TABLE `garment` ADD COLUMN wip_load DECIMAL(5,2) AS (`wip`/`no_of_workers`);
ALTER TABLE `garment` ADD COLUMN productivity_per_worker DECIMAL(5,2) AS (`actual_productivity`*`smv`/`no_of_workers`);
ALTER TABLE `garment` ADD COLUMN overtime_per_worker DECIMAL(5,2) AS (`over_time`/`no_of_workers`);
ALTER TABLE `garment` ADD COLUMN yearweek INT AS (YEARWEEK(STR_TO_DATE(date,'%Y-%m-%d'),1))VIRTUAL;


-- 資料清洗

UPDATE garment												-- 改department拼字錯誤
SET department = 'sewing'
WHERE department = 'sweing';

UPDATE `garment`											-- 改日期的格式	
SET `date` = DATE_FORMAT(STR_TO_DATE(`date`,'%m/%d/%Y'), '%Y-%m-%d');
UPDATE `garment` SET `date` = TRIM(`date`);
ALTER TABLE `garment` MODIFY COLUMN `date` DATE;

UPDATE `garment` SET department = TRIM(department);

-- Team's efficiency gap heatmap 

SELECT 
    `team`, 
    YEARWEEK(STR_TO_DATE(`date`, '%Y-%m-%d'), 1) AS `work_week`, -- 取得年與週
    ROUND(AVG(`efficiency_gap`), 3) AS `avg_gap`
FROM `garment`
GROUP BY `team`, `work_week`
ORDER BY `work_week`, `team`;


-- Productivity trend bar chart

SELECT 
    YEARWEEK(STR_TO_DATE(`date`, '%Y-%m-%d'), 1) AS `work_week`, -- 取得年與週
    ROUND(AVG(`efficiency_gap`), 3) AS `avg_gap`
FROM `garment`
GROUP BY `work_week`
ORDER BY `work_week`;


-- 第8,9週生產力異常：兩起該週最高的idle_men事件都是發生在team 10

SELECT *
FROM `garment`
WHERE `yearweek` IN (201508,201509) 
ORDER BY `date` ASC;

SELECT Count(*) 				-- idle_men比例在這兩週佔近整體的2/3 (11/18)
FROM `garment`
WHERE idle_men != 0 AND yearweek IN (201508,201509)
;


-- Team 10 第8週生產力異常原因：兩起該週最高的idle_men事件都是發生在team 10

SELECT `date`, `team`, smv, wip, over_time, idle_time, idle_men, no_of_workers, efficiency_gap, wip_load, overtime_per_worker
FROM `garment`
WHERE `yearweek` = 201508 AND `team` = 10  
ORDER BY `date` ASC;

SELECT * 						-- 兩起該週最高的idle_men事件都是發生在team 10
FROM `garment`
WHERE yearweek = 201508 AND idle_men != 0;


-- Team 1,3

SELECT team, COUNT(*) -- team 1,3都沒有idle_men的問題發生
FROM `garment`
WHERE idle_men != 0
GROUP by team;


