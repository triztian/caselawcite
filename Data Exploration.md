# Commands and Steps related to Data Exploration

For the purposes of simplicity we will use the bash variables `$DATA` and `$DPROC`
to contain the paths to the _raw data_ directory and file based processed data
respectively.

```bash
# pwd points to the root of our project repo
export DATA=$(pwd)/Data/Illinois-20200302-text/data
export DPROC=$(pwd)/Data/Processed
```

#### Extracting the Bulk Download

```bash
xzcat $DATA/data.jsonl.xz > data.jsonl
```

#### Converting from JSON Line (`*.jsonl`) to a regular JSON array

The compressed file contains records in JSON line format, meaning that 
each JSON Object is delimited by a newline instead if a comma, i.e. instead
of:

```json
[
	{"id": 0},
	{"id": 1}
]
```

We have:

```
{"id": 0}
{"id": 1}
```
The JSONL format will cause issues in our `jq` filters, to convert it we can use 
the "slurp" feature of `jq`:

```bash
cd ./Data/Illinois-20200302-text
jq -s $DATA/data.jsonl > $DPROC/data.json
```

#### Creating a JSON schema (for Case Objects)

First get the first record of the case data:

```bash
jq '.[0]' $DATA/data.json > $DPROC/data_0.json
```

Then after we've extracted the first case, lets generate a schema from it:

```bash
cd ./Data/Illinois-20200302-text
genson $DPROC/data_0.json > $DPROC/data_0_schema.json
```

#### Sampling down the data for quicker ETL prototyping

To reduce our ETL iteration speed it's a good idea to reduce the size of our 
data set, for our project we've

```bash
jq '.[:200]' $DATA/data.json > $DPROC/data_first_200.json
```