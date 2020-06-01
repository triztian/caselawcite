#!/usr/bin/env python3

import sys
import argparse

import do_create_tables as create_tables
import do_create_attorneys as create_attorneys
import do_create_cases as create_cases
import do_create_citations as create_citations

parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers()
create_parser = subparsers.add_parser("create")

create_subparser = create_parser.add_subparsers(dest="command")
create_subparser.add_parser("tables", parents=[create_tables.parser], add_help=False)
create_subparser.add_parser(
    "attorneys", parents=[create_attorneys.parser], add_help=False
)
create_subparser.add_parser("cases", parents=[create_cases.parser], add_help=False)
create_subparser.add_parser("citations", parents=[create_citations.parser], add_help=False)

if __name__ == "__main__":
    args = parser.parse_args()

    if args.command == "tables":
        create_tables.run(args)

    elif args.command == "attorneys":
        create_attorneys.run(args)

    elif args.command == "cases":
        create_cases.run(args)

    elif args.command == "citations":
        create_citations.run(args)
