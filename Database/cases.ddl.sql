CREATE TABLE IF NOT EXISTS cases (
	id PRIMARY KEY INTEGER,
	docket_number TEXT NOT NULL,
	jurisdiction TEXT NOT NULL,
	court TEXT NOT NULL,
	volume INTEGER NOT NULL,
	first_page INTEGER NOT NULL,
	last_page INTEGER NOT NULL,
	decision_date DATE NOT NULL,
	url TEXT
);

CREATE TABLE IF NOT EXISTS case_citations (
	case_id 			INTEGER NOT NULL,
	cites_to_case_id	INTEGER NOT NULL
);