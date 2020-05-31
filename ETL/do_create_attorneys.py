#!/usr/bin/env python3

import sys
import os
import sqlite3
import argparse
import logging

from data_loading import *
from attorney_names import *


parser = argparse.ArgumentParser(
    description='Extract the ".casebody.data.attorneys" of each case'
)

parser.add_argument(
    "sqlite_path",
    metavar="sqlite_path",
    type=str,
    help="Path to the SQLite database where the information will be stored",
)

parser.add_argument(
    "data_path", metavar="data_path.json", type=str, help="Path to the JSON data file"
)

parser.add_argument(
    "-p", "--print", type=int, help="Only print the names, don't store them"
)


def store_in_sqlitedb(dbpath, cases):
    """Store the attorney case data in the sqlite db"""
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
                cur.execute(insert_stmt, (attorney["names"],))
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
    with open(args.data_path, "r") as f:
        objects = load_attorney_names_text(f)

        if args.sqlite_path:
            store_in_sqlitedb(args.sqlite_path, objects)
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
