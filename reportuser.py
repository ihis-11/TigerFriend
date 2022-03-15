#!/usr/bin/env python

# -----------------------------------------------------------------------
# create.py
# Author: Bob Dondero
# -----------------------------------------------------------------------

from sys import argv, stderr, exit
from contextlib import closing
from sqlite3 import connect

# -----------------------------------------------------------------------

DATABASE_URL = 'file:TigerFriend.sqlite?mode=rwc'


def report_user(reporter_net_id, reported_net_id, report_type, report_comment):
    try:
        with connect(DATABASE_URL, isolation_level=None,
                     uri=True) as connection:

            with closing(connection.cursor()) as cursor:

                # ------------------------------------------------------

                stmt_str = "INSERT INTO reports "
                stmt_str += "(reporter_net_id, reporter_net_id, "
                stmt_str += "report_type, report_comment) "
                stmt_str += "VALUES (?,?,?,?)"

                cursor.execute(stmt_str, [reporter_net_id, reported_net_id,
                                          report_type, report_comment])

                # ------------------------------------------------------

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)


def main():
    # test
    report_user('Tester', 'Bully', 'Harassment', 'This person was mean to me.')


# -----------------------------------------------------------------------

if __name__ == '__main__':
    main()
