#!/usr/bin/env python

# --------------------------------------------------------------------
# admin_sql
# --------------------------------------------------------------------

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configs
from database import Administrators, Reports
from sys import stderr

DATABASE_URL = configs.DATABASE_URL


def is_admin(net_id):
    # connect to database
    try:
        engine = create_engine(DATABASE_URL)

        Session = sessionmaker(bind=engine)
        session = Session()

        admin = (session.query(Administrators)
                 .filter(Administrators.net_id == net_id)
                 .one_or_none())

        if admin is not None:
            return True
        return False

    except Exception as ex:
        print(ex, file=stderr)
        print("Admin check failed", file=stderr)

# Returns [reported, reportee, type, comment] of a certain report
def get_report(rep_id):
    # connect to database
    try:
        engine = create_engine(DATABASE_URL)

        Session = sessionmaker(bind=engine)
        session = Session()

        report = (session.query(Reports)
                 .filter(Reports.report_id == rep_id)
                 .one_or_none())

        return [report.reported_net_id, report.reporter_net_id, report.type, report.comment]

    except Exception as ex:
        print(ex, file=stderr)
        print("Admin check failed", file=stderr)

# unit test
def main():
    myself = 'collado'
    print(myself + " is admin: " + str(is_admin(myself)))
    not_admin = 'notanadmin'
    print(not_admin + " is admin: " + str(is_admin(not_admin)))


# ----------------------------------------------------------------------


if __name__ == '__main__':
    main()
