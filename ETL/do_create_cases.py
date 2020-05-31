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
    "sqlite_path", metavar="sqlite_path", type=str, help="Path to the SQLite database to use (with tables)"
)

parser.add_argument(
    "data_path", metavar="data_path_json", type=str, help="Path to the JSON data file"
)


def store_in_sqlitedb(dbpath, cases):
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


def run(args):
    with open(args.data_path, "r") as f:
        objects = load_cases(f)
        store_in_sqlitedb(args.sqlite_path, objects)
