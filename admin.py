#!/usr/bin/env python

import random
# --------------------------------------------------------------------
# chat_sql.py
# --------------------------------------------------------------------
from datetime import datetime
from sys import stderr

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

import configs
from account_sql import get_user_bio, get_netid
from database import Administrators

DATABASE_URL = configs.DATABASE_URL


# --------------------------------------------------------------------

# Takes user (net_id) and returns a bool of whether they are an admin
def is_admin(user):
    try:
        # connect to database
        engine = create_engine(DATABASE_URL)

        Session = sessionmaker(bind=engine)
        session = Session()

        admin = (session.query(Administrators)
                 .filter(Administrators.net_id == user)
                 .all())

        if not admin:
            return False
        else:
            return True

    except Exception as ex:
        session.close()
        engine.dispose()
        print(ex, file=stderr)
        print("Data base connection failed", file=stderr)
        return "unknown (database connection failed)"


# unit test
def main():
    myself = 'collado'
    print(myself + " is admin: " + str(is_admin(myself)))
    not_admin = 'notanadmin'
    print(not_admin + " is admin: " + str(is_admin(not_admin)))


# ----------------------------------------------------------------------


if __name__ == '__main__':
    main()
