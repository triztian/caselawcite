#!/bin/bash

rm -fv ${1}

./ETL/hcapetl.py create tables ${1} ./Database/*.ddl.sql
./ETL/hcapetl.py create attorneys ${1} ./Data/Processed/data.json
./ETL/hcapetl.py create cases ${1} ./Data/Processed/data.json
./ETL/hcapetl.py create citations ${1} ./Data/Processed/data.json