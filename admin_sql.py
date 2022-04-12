#!/usr/bin/env python

# --------------------------------------------------------------------
# admin_sql
# --------------------------------------------------------------------

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configs
from database import Administrators
from sys import stderr

DATABASE_URL = configs.DATABASE_URL

def isAdmin(net_id):
    # connect to database
    try:
        engine = create_engine(DATABASE_URL)

        Session = sessionmaker(bind=engine)
        session = Session()

        admin = (session.query(Administrators)
                .filter(Administrators.net_id == net_id)
                .all())

        if admin != []:
            return True
        return False

    except Exception as ex:
        print(ex, file=stderr)
        print("Admin check failed", file=stderr)