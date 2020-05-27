.headers on
.mode column

SELECT 
	attorney_id, 
	names, 
	COUNT(*) as case_count 
FROM 
	attorney_cases 
	INNER JOIN attorneys ON attorneys.id = attorney_id 
GROUP BY 
	attorney_id 
ORDER BY case_count DESC 
LIMIT 50;