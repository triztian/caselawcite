#!/usr/bin/env python3

import sys
import os
import sqlite3
import argparse
import logging
import csv

from data_loading import *
from cases import *


command = argparse.ArgumentParser(
    description='Extract the Case data'
)

command.add_argument(
    "DataPath", metavar="data_path.json", type=str, help="Path to the JSON data file"
)

command.add_argument(
    "-s", "--sqlite", type=str, help="Path to the SQLite3 DB to be used"
)

command.add_argument(
    "-t",
    "--tables-ddl",
    type=str,
    help="Path to the SQL DDL file that setups the tables",
)

command.add_argument(
    "-d",
    "--drop-tables",
    type=str,
    help="Path to the SQL DDL file that setups the tables",
)

command.add_argument(
    "-c", "--citations", 
     action='store_true',
     help="Create citations instead of case entries"
)

command.add_argument(
    "-l", "--log-level", type=str, help="The log level; default is warning"
)


def setup_tables(dbpath, tables_ddl_path):
    """Creates SQLite tables for cases"""
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    with open(tables_ddl_path, "r") as f:
        ddl = f.read()
        for stmt in ddl.split(";"):
            if not stmt:
                continue
            logging.debug(f"Table stmt: {stmt}")
            cur.execute(stmt)
        conn.commit()
        conn.close()


def store_in_sqlitedb(dbpath, tables_ddl_path, cases):
    """Store the case data in the sqlite db"""
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    for case in cases:
        case = sanitize_case(case)
        insert_stmt = "INSERT INTO cases VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

        cur.execute(
            insert_stmt,
            (
                case["id"],
                case["jurisdiction"],
                case["court"],
                case["volume"],
                case["first_page"],
                case["last_page"],
                case["decision_date"],
                case["url"],
            ),
        )

    conn.commit()
    conn.close()


def store_in_sqlitedb_citations(dbpath, citations_path):
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    with open(citations_path, 'r') as f:
        cits_reader = csv.reader(f, delimiter=',')
        insert_stmt = "INSERT INTO case_citations VALUES (?, ?)"
        for row in cits_reader:
            case_id = int(row[0])
            for cited_case_id in row[1:]:
                cur.execute(insert_stmt, (row[0], cited_case_id))

    conn.commit()
    conn.close()


def run(args):
    if args.log_level:
        logging.basicConfig(level=getattr(logging, args.log_level.upper()))

    if args.drop_tables and args.tables_ddl:
        pass

    if not args.citations:
        with open(args.DataPath, "r") as f:
            objects = load_cases(f)

            if args.sqlite:
                setup_tables(args.sqlite, args.tables_ddl)
                store_in_sqlitedb(args.sqlite, args.tables_ddl, objects)
                return

            max_print = 12
            if args.print:
                max_print = args.print

            read = 0
            for obj in objects:
                print(obj)
                read += 1
                if read > max_print:
                    return
    else:
        store_in_sqlitedb_citations(args.sqlite, args.DataPath)


if __name__ == "__main__":
    run(command.parse_args())
