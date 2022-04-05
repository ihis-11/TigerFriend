#!/usr/bin/env python

# --------------------------------------------------------------------
# chat_sql.py
# --------------------------------------------------------------------
from cgitb import reset
from datetime import datetime
import random
from sys import stderr

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database import Chats, Account, Messages

from account_sql import get_user_bio, get_netid

DATABASE_URL = 'postgresql://fpzzhwdkkymqrr:b87ef0b3ae33d79f063d25d7ec8dde6871405d7d85b67ddff7f1ddaec3d00361@ec2-3-217-113-25.compute-1.amazonaws.com:5432/dd4c5lulvqtkld'

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

    except (Exception) as ex:
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

        matchid = get_netid(str(match))
        print(matchid)
        if matchid is None:
            return "No match username found"
        
        chats = (session.query(Chats)
                .filter((Chats.net_id1 == user) | (Chats.net_id2 == user))
                .all())

        chatid = None
        for chat in chats:
            if ((str(chat.net_id1) == (matchid)) | (str(chat.net_id2) == str(matchid))):
                chatid = chat.chat_id
                break
        if chatid is None:
            chatid = __insert_chat_id__(user, matchid)

        session.close()
        engine.dispose()
        return chatid

    except (Exception) as ex:
        session.close()
        engine.dispose()
        print(ex, file=stderr)
        print("Data base connection failed", file=stderr)
        return "unknown (database connection failed)"

# helper method for get_chat_id
def __insert_chat_id__(user, match):
    try:
        # connect to database
        engine = create_engine(DATABASE_URL)
         
        Session = sessionmaker(bind=engine)
        session = Session()

        id = str(random.randint(1000, 9999))
        chats = (session.query(Chats)
                .filter(Chats.chat_id == id)
                .all())
        while chats != []:
            id = str(random.randint(1000, 9999))
            chats = (session.query(Chats)
                    .filter(Chats.chat_id == id)
                    .all())

        newChat = Chats(net_id1 = user,
                        net_id2 = match,
                        chat_id = id)

        session.add(newChat)
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

        newMessage = Messages(chat_id = chat_id,
                                sender_id = sender,
                                message_content = message,
                                date_time = now)

        session.add(newMessage)
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
