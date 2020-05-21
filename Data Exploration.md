# Commands and Steps related to Data Exploration


#### Extracting the Bulk Download

```bash
xzcat ./Data/Illinois-20200302-text/data/data.jsonl.xz > data.jsonl
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
jq -s ./data/data.jsonl > ./data/data.json
```

#### Creating a JSON schema (for Case Objects)

First get the first record of the case data:

```bash
cd ./Data/Illinois-20200302-text
jq '.[0]' ./data/data.json > data_0.json
```

Then after we've extracted the first case, lets generate a schema from it:

```bash
cd ./Data/Illinois-20200302-text
genson ./data/data_0.json > data_0_schema.json
```