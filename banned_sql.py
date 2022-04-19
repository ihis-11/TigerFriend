#!/usr/bin/env python

# --------------------------------------------------------------------
# banned_sql
# --------------------------------------------------------------------

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import configs
from database import Banned
from sys import stderr

DATABASE_URL = configs.DATABASE_URL

def is_banned(net_id):
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

def add_ban(banned, time):
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

def get_days(net_id):
    try:
        engine = create_engine(DATABASE_URL)

        Session = sessionmaker(bind=engine)
        session = Session()

        ban = (session.query(Banned)
                .filter(Banned.net_id == net_id)
                .one_or_none())
        
        session.close()
        engine.dispose()

        return ban.days_left

    except Exception as ex:
        print(ex, file=stderr)
        print("Banned add failed", file=stderr)
