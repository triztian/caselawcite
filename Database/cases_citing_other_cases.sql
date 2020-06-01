SELECT 
	case_id, count(*)
FROM 
	case_citations 
WHERE
	cites_to_case_id IN (
		SELECT case_id FROM attorney_cases WHERE attorney_id = 13938
	)
GROUP BY
	case_id