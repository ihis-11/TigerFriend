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
from database import Chats, Account, Messages

DATABASE_URL = configs.DATABASE_URL


# --------------------------------------------------------------------

# Takes user (net_id) and returns the list of usernames they have open
# chats with. SHOULDN'T RETURN DUPLICATES
def get_all_chats(user):
    try:
        # connect to database
        engine = create_engine(DATABASE_URL)

        Session = sessionmaker(bind=engine)
        session = Session()

        chats = (session.query(Chats).filter((Chats.net_id1 == user) | (Chats.net_id2 == user)).all())

        other_ids = []
        for chat in chats:
            if chat.net_id1 == user:
                other_ids.append(chat.net_id2)
            else:
                other_ids.append(chat.net_id1)

        other_users = []
        for other in other_ids:
            users = (session.query(Account)
                     .filter(Account.net_id == other)
                     .all())
            other_users.append(str(users[0].username))

        session.close()
        engine.dispose()
        return other_users

    except Exception as ex:
        session.close()
        engine.dispose()
        print(ex, file=stderr)
        print("Data base connection failed", file=stderr)
        return "unknown (database connection failed)"


# Takes user (net_id) and their match (username), and returns their
# chat_id. Makes a new one and inserts if it doesn't exist in the table.
def get_chat_id(user, match):
    try:
        engine = create_engine(DATABASE_URL)

        Session = sessionmaker(bind=engine)
        session = Session()

        matchid = get_netid(match)
        if matchid is None:
            return "No match username found"

        chats = (session.query(Chats)
                 .filter((Chats.net_id1 == user) | (Chats.net_id2 == user))
                 .all())

        chatid = None
        for chat in chats:
            if (str(chat.net_id1) == matchid) | (str(chat.net_id2) == str(matchid)):
                chatid = chat.chat_id
                break
        if chatid is None:
            print("will insert")
            chatid = __insert_chat_id__(user, matchid)

        session.close()
        engine.dispose()
        return chatid

    except Exception as ex:
        session.close()
        engine.dispose()
        print(ex, file=stderr)
        print("Data base connection failed", file=stderr)
        return "unknown (database connection failed)"


# helper method for get_chat_id
def __insert_chat_id__(user, matchid):
    try:
        # connect to database
        engine = create_engine(DATABASE_URL)

        Session = sessionmaker(bind=engine)
        session = Session()

        new_id = str(random.randint(1000, 9999))
        chats = (session.query(Chats)
                 .filter(Chats.chat_id == new_id)
                 .all())
        while chats:
            new_id = str(random.randint(1000, 9999))
            chats = (session.query(Chats)
                     .filter(Chats.chat_id == new_id)
                     .all())

        new_chat = Chats(net_id1=user,
                         net_id2=matchid,
                         chat_id=new_id)

        session.add(new_chat)
        session.commit()

        session.close()
        engine.dispose()
        return id

    except Exception as ex:
        session.close()
        engine.dispose()
        print(ex, file=stderr)
        print("Data base connection failed", file=stderr)
        return "unknown (database connection failed)"


# Takes chat_id, message content, and sender (net_id), and adds to
# database
def send_chat(chat_id, sender, message):
    try:
        engine = create_engine(DATABASE_URL)

        Session = sessionmaker(bind=engine)
        session = Session()

        now = str(datetime.now())

        new_message = Messages(chat_id=chat_id,
                               sender_id=sender,
                               message_content=message,
                               date_time=now)

        session.add(new_message)
        session.commit()

        session.close()
        engine.dispose()

    except Exception as ex:
        session.close()
        engine.dispose()
        print(ex, file=stderr)
        print("Data base connection failed", file=stderr)
        return "unknown (database connection failed)"


# get all message history from a given chat_id
def get_messages(chat_id):
    try:
        engine = create_engine(DATABASE_URL)

        Session = sessionmaker(bind=engine)
        session = Session()

        chats = (session.query(Messages)
                 .filter(Messages.chat_id == chat_id)
                 .order_by(desc(Messages.date_time))
                 .all())

        chat_history = []
        for chat in chats:
            user = get_user_bio(chat.sender_id)[0]
            chat_history.append((user, str(chat.message_content), str(chat.date_time)))

        session.close()
        engine.dispose()

        return chat_history

    except Exception as ex:
        session.close()
        engine.dispose()
        print(ex, file=stderr)
        print("Data base connection failed", file=stderr)
        return "unknown (database connection failed)"


# unit test
def main():
    myself = 'collado'
    chats = get_all_chats(myself)
    print(chats)
    id1 = get_chat_id(myself, 'haha371')
    print(id1)
    id2 = get_chat_id(myself, 'Kenny')
    print(id2)
    send_chat(id1, myself, 'hello person 1')
    send_chat(id2, myself, 'hello person 2')
    msgs1 = get_messages(id1)
    print(msgs1)
    msgs2 = get_messages(id2)
    print(msgs2)


# ----------------------------------------------------------------------


if __name__ == '__main__':
    main()
