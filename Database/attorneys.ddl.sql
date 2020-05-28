CREATE TABLE IF NOT EXISTS "attorneys" (
	id 		INTEGER PRIMARY KEY AUTOINCREMENT,
	names	TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS "attorney_cases" (
	attorney_id INTEGER NOT NULL,
	case_id 	INTEGER NOT NULL,
	party 		TEXT,
	party_type	TEXT,
	title		TEXT,
	PRIMARY KEY(attorney_id, case_id)
);