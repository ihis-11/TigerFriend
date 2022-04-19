#!/usr/bin/env python

# --------------------------------------------------------------------
# banned_sql
# --------------------------------------------------------------------

from sqlalchemy import create_engine, true
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, desc
import configs
from database import Administrators, Banned, Reports, Messages
from sys import stderr

DATABASE_URL = configs.DATABASE_URL

def isBanned(net_id):
    # connect to database
    try:
        engine = create_engine(DATABASE_URL)

        Session = sessionmaker(bind=engine)
        session = Session()

        ban = (session.query(Banned)
                 .filter(Banned.net_id == net_id)
                 .one_or_none())

        session.close()
        engine.dispose()

        if ban is not None:
            return True
        return False

    except Exception as ex:
        print(ex, file=stderr)
        print("Banned check failed", file=stderr)

def addBan(banned, time):
    # connect to database
    try:
        engine = create_engine(DATABASE_URL)

        Session = sessionmaker(bind=engine)
        session = Session()

        ban = (session.query(Banned)
                 .filter(Banned.net_id == banned)
                 .one_or_none())

        if ban is not None:
            ban.days_left += time
            
        else:
            new_ban = Banned(net_id=banned, days_left=time)
            session.add(new_ban)

        session.commit()
        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        print("Banned add failed", file=stderr)
