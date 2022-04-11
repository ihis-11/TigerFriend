#!/usr/bin/env python

from sys import stderr
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import configs
from database import Account

DATABASE_URL = configs.DATABASE_URL


def api_account_creation(net_id, year, maj, res, user, bio):
    try:
        engine = create_engine(DATABASE_URL)

        Session = sessionmaker(bind=engine)
        session = Session()

        new_account = Account(net_id=net_id,
                              username=user,
                              class_year=year,
                              major=maj,
                              bio_string=bio,
                              res_college=res)

        session.add(new_account)
        session.commit()

        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        print("Account creation failed", file=stderr)


def update_bio(net_id, bio):
    try:
        engine = create_engine(DATABASE_URL)

        Session = sessionmaker(bind=engine)
        session = Session()

        update = (session.query(Account)
                  .filter(Account.net_id == net_id)
                  .one())
        update.bio_string = bio

        session.commit()
        session.close()
        engine.dispose()
        print("Record inserted successfully into account")

    except Exception as ex:
        print(ex, file=stderr)
        print("Update bio failed", file=stderr)


# update net_id's new username to user
def update_username(net_id, user):
    try:
        engine = create_engine(DATABASE_URL)

        Session = sessionmaker(bind=engine)
        session = Session()

        update = (session.query(Account)
                  .filter(Account.net_id == net_id)
                  .one())
        update.username = user

        session.commit()
        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        print("Update username failed", file=stderr)


# to get net_id from username
def get_netid(user):
    engine = create_engine(DATABASE_URL)

    Session = sessionmaker(bind=engine)
    session = Session()

    user = (session.query(Account)
            .filter(Account.username == user)
            .all())

    session.close()
    engine.dispose()
    if not user:
        return None
    return user[0].net_id


# to get bio for the chat
def get_bio(username):
    try:
        engine = create_engine(DATABASE_URL)

        Session = sessionmaker(bind=engine)
        session = Session()

        user = (session.query(Account)
                .filter(Account.username == username)
                .all())

        session.close()
        engine.dispose()
        if not user:
            return "No user with this username"
        return user[0].bio_string
    except Exception as ex:
        print(ex, file=stderr)
        print("No user with this username", file=stderr)


# returns year and major
def get_year_major(net_id):
    try:
        engine = create_engine(DATABASE_URL)

        Session = sessionmaker(bind=engine)
        session = Session()

        user = (session.query(Account)
                .filter(Account.net_id == net_id)
                .all())

        session.close()
        engine.dispose()
        if not user:
            return ["unknown (" + net_id + " not found)", "?"]
        return [user[0].class_year, user[0].major]
    except Exception as ex:
        print(ex, file=stderr)
        print("Data base connection failed", file=stderr)
        return ["unknown (database connection failed)", "unknown"]


# returns user and bio, None if account doesn't exist
def get_user_bio(net_id):
    try:
        engine = create_engine(DATABASE_URL)

        Session = sessionmaker(bind=engine)
        session = Session()

        user = (session.query(Account)
                .filter(Account.net_id == net_id)
                .all())

        session.close()
        engine.dispose()
        if not user:
            return None
        return [user[0].username, user[0].bio_string]

    except Exception as ex:
        print(ex, file=stderr)
        print("Data base connection failed", file=stderr)
        return ["unknown (database connection failed)", "unknown"]


def delete():
    try:
        engine = create_engine(DATABASE_URL)

        Session = sessionmaker(bind=engine)
        session = Session()

        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        print("Data base connection failed", file=stderr)
        return ["unknown (database connection failed)", "unknown"]
