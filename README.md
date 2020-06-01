# UCLACaseLawCite

Final project for UCLA's Data Science - Exploratory Data Analysis and Visualization


## Obtaining the Data

### Bulk case data

Bulk case data can be downloaded from the following URL:

  * [Download Page](https://case.law/bulk/download/)
  * [Direct Link (465 MB)](https://api.case.law/v1/bulk/22341/download/)


```bash
mkdir Data && cd Data
curl https://api.case.law/v1/bulk/22341/download/
```

### Case citations

Citation can be found here:

  * [Download Page](https://case.law/download/citation_graph/)
  * [Direct Link (165 MB)](https://case.law/download/citation_graph/2020-04-28/citations.csv.gz)


```bash
cd Data/Illinois-20200302-text/data
curl https://case.law/download/citation_graph/2020-04-28/citations.csv.gz
```

## Preparing the Data for analysis

After downloading the data into the `Data` directory we can use the 
python script included in `./ETL/hcapetl.py` directory to transform, clean and insert
the data into a SQLite database that will simplify our analysis.

The database will be named `hcap.sqlite` and it can be created by the following 
commands:

```bash
dbpath=./hcap.sqlite

./ETL/hcapetl.py create tables "$dbpath" ./Database/*.ddl.sql
./ETL/hcapetl.py create attorneys "$dbpath" ./Data/Processed/data.json
./ETL/hcapetl.py create cases "$dbpath" ./Data/Processed/data.json
./ETL/hcapetl.py create citations "$dbpath" ./Data/Processed/data.json
```

The previous commands can be found in the `gendata.sh` script at the root of
this project.

The `ETL` directory has all of the python source necessary to work with the data.
To aid with the exploration and cleanup we have the following Jupyter Notebooks:

  1. [Attorney Name Parsing]("./Attorney Name Parsing.ipynb")
  2. [Attorney Record Parsing]("./Attorney Record Parsing.ipynb")
  3. [Attorney Career Overview]("./Attorney Career Overview.ipynb")

## Analysis

