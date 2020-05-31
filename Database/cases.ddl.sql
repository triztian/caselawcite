CREATE TABLE IF NOT EXISTS cases (
	id 				INTEGER PRIMARY KEY,
	-- docket_number 	INTEGER NOT NULL,
	jurisdiction 	TEXT NOT NULL,
	court 			TEXT NOT NULL,
	volume 			INTEGER NOT NULL,
	first_page 		INTEGER NOT NULL,
	last_page 		INTEGER NOT NULL,
	decision_date 	DATE NOT NULL,
	url TEXT
);

CREATE TABLE IF NOT EXISTS case_citations (
	case_id 			INTEGER NOT NULL,
	cites_to_case_id	INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS case_docket_numbers (
	case_id 		INTEGER NOT NULL,
	docket_number 	INTEGER NOT NULL,
	PRIMARY KEY(case_id, docket_number)
);
