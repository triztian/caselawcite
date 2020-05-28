#!/usr/bin/env python3

import sys
import os
import sqlite3
import argparse
import logging

from data_loading import *
from attorney_names import *


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
    """Creates SQLite tables for attorneys"""
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
    """Store the attorney case data in the sqlite db"""
    setup_tables(dbpath, tables_ddl_path)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    for case in cases:
        case_id = case["id"]
        attorneys = parse_attorneys(case["attorneys"])
        for attorney in attorneys:
            insert_stmt = "INSERT INTO attorneys (names) VALUES (?)"
            attorney_id = None
            try:
                logging.info(f"Insert STMT: {insert_stmt}")
                cur.execute(insert_stmt, (attorney["name"],))
                logging.info(cur.lastrowid)

                attorney_id = cur.lastrowid
            except Exception as e:
                logging.info(str(e))
                cur.execute(
                    "SELECT id FROM attorneys WHERE names = ? LIMIT 1",
                    (attorney["names"],),
                )
                result = cur.fetchone()
                if result:
                    attorney_id = result[0]

            insert_stmt = "INSERT INTO attorney_cases VALUES (?, ?, ?, ?, ?)"
            try:
                logging.info(f"Insert STMT: {insert_stmt}")
                cur.execute(
                    insert_stmt,
                    (
                        attorney_id,
                        case_id,
                        attorney["party"],
                        attorney["party_type"],
                        attorney["title"],
                    ),
                )
            except Exception as e:
                logging.info(str(e))

    conn.commit()
    conn.close()


def run(args):
    if args.log_level:
        logging.basicConfig(level=getattr(logging, args.log_level.upper()))

    with open(args.DataPath, "r") as f:
        objects = load_attorney_names_text(f)

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
