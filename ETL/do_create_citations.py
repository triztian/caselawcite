#!/usr/bin/env python3

import sys
import os
import sqlite3
import argparse
import logging
import csv

from data_loading import *
from cases import *


parser = argparse.ArgumentParser(description="Extract the Case data")

parser.add_argument(
    "sqlite_path", metavar="sqlite_path", type=str, help="Path to the SQLite db to use (the tables must already exist)"
)

parser.add_argument(
    "citations_path", metavar="citations_csv_path", type=str, help="Path to the CSV citations data file"
)


def store_in_sqlitedb_citations(dbpath, citations_path):
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    with open(citations_path, "r") as f:
        cits_reader = csv.reader(f, delimiter=",")
        insert_stmt = "INSERT INTO case_citations VALUES (?, ?)"
        for row in cits_reader:
            case_id = int(row[0])
            for cited_case_id in row[1:]:
                cur.execute(insert_stmt, (row[0], cited_case_id))

    conn.commit()
    conn.close()


def run(args):
    store_in_sqlitedb_citations(args.sqlite_path, args.citations_path)


if __name__ == "__main__":
    run(parser.parse_args())
