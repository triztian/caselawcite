#!/usr/bin/env python3

import sys
import os
import sqlite3
import argparse
import logging

from data_loading import *
from cases import *


command = argparse.ArgumentParser(
    description='Extract the ".casebody.data.attorneys" of each case'
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
    "-p", "--print", type=int, help="Only print the names, don't store them"
)

command.add_argument("-c", "--clean", type=int, help="Clean / overwrite the SQLite DB")

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
    setup_tables(dbpath, tables_ddl_path)
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


def run(args):
    if args.log_level:
        logging.basicConfig(level=getattr(logging, args.log_level.upper()))

    with open(args.DataPath, "r") as f:
        objects = load_cases(f)

        if args.sqlite:
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


if __name__ == "__main__":
    run(command.parse_args())
