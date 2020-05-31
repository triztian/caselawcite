import argparse
import logging
import sqlite3

parser = argparse.ArgumentParser()
parser.add_argument(
    "sqlite_path", metavar="sqlite_path", type=str, help="Path to the database file"
)
parser.add_argument(
    "ddl_paths",
    metavar="ddl_paths",
    nargs="+",
    type=str,
    help="DDL files to create tables",
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


def run(args):
    for ddl_path in args.ddl_paths:
        setup_tables(args.sqlite_path, ddl_path)
