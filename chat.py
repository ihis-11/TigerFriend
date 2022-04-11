# --------------------------------------------------------------------
# chat.py
# --------------------------------------------------------------------
import random
from datetime import datetime
from sys import stderr

import psycopg2

from RawData_SQL import get_account_details

DATABASE_URL = 'file:TigerFriend.sqlite?mode=ro'


# --------------------------------------------------------------------

# Takes user (net_id) and returns the list of usernames they have open
# chats with.
def get_all_chats(user):
    try:
        # connect to database
        with psycopg2.connect(host="ec2-3-217-113-25.compute-1.amazonaws.com",
                              database="dd4c5lulvqtkld",
                              user="fpzzhwdkkymqrr",
                              password="b87ef0b3ae33d79f063d25d7ec8dde6871405d7d85b67ddff7f1ddaec3d00361") as connect:
            with connect.cursor() as cursor:

                stmt = "SELECT * FROM chats WHERE net_id1=\'" + \
                       user + "\' OR net_id2=\'" + user + "\'"
                cursor.execute(stmt)
                chats = cursor.fetchone()
                other_users = []

                while chats is not None:
                    if str(chats[0]) == user:
                        # print(str(chats[1]) + " is chatting with " + user)
                        other_users.append(str(chats[1]))
                    else:
                        # print(str(chats[0]) + " is chatting with " + user)
                        other_users.append(str(chats[0]))
                    chats = cursor.fetchone()

                i = 0
                for other in other_users:
                    stmt = "SELECT username FROM account WHERE net_id=\'" + other + "\'"
                    cursor.execute(stmt)
                    other_user = cursor.fetchone()
                    other_users[i] = other_user[0]
                    i += 1

                return other_users

    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)
        print("Data base connection failed", file=stderr)
        return ["unknown (database connection failed)", "unknown"]


# Takes user (net_id) and their match (username), and returns their
# chat_id. Makes a new one and inserts if it doesn't exist in the table.
def get_chat_id(user, match):
    try:
        # connect to database
        with psycopg2.connect(host="ec2-3-217-113-25.compute-1.amazonaws.com",
                              database="dd4c5lulvqtkld",
                              user="fpzzhwdkkymqrr",
                              password="b87ef0b3ae33d79f063d25d7ec8dde6871405d7d85b67ddff7f1ddaec3d00361") as connect:
            with connect.cursor() as cursor:
                stmt = "SELECT net_id FROM account WHERE username=\'" + match + "\'"
                cursor.execute(stmt)
                match = cursor.fetchone()
                if match is None:
                    # print("No match username found", file=stderr)
                    return "No match username found"
                match = str(match[0])
                # print("Match's net_id: " + match)

                stmt = "SELECT * FROM chats WHERE net_id1=\'" + \
                       user + "\' OR net_id2=\'" + user + "\'"
                cursor.execute(stmt)
                chats = cursor.fetchone()
                chat_id = None
                while chats is not None:
                    # print("Chat_id found: " + str(chats[2]))
                    if str(chats[0]) == match or str(chats[1]) == match:
                        # print("Match!")
                        chat_id = str(chats[2])
                        break
                    chats = cursor.fetchone()
                if chat_id is None:
                    # print("making new chat")
                    __insert_chat_id__(user, match)

                return chat_id

    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)
        print("Data base connection failed", file=stderr)
        return ["unknown (database connection failed)", "unknown"]


# helper method for get_chat_id
def __insert_chat_id__(user, match):
    try:
        # connect to database
        with psycopg2.connect(host="ec2-3-217-113-25.compute-1.amazonaws.com",
                              database="dd4c5lulvqtkld",
                              user="fpzzhwdkkymqrr",
                              password="b87ef0b3ae33d79f063d25d7ec8dde6871405d7d85b67ddff7f1ddaec3d00361") as connect:
            with connect.cursor() as cursor:
                chat_id = str(random.randint(1000, 9999))
                stmt = "SELECT chat_id FROM chats WHERE chat_id=\'" + chat_id + "\'"
                cursor.execute(stmt)
                chat = cursor.fetchone()
                while chat is not None:
                    chat_id = str(random.randint(1000, 9999))
                    stmt = "SELECT chat_id FROM chats WHERE chat_id=\'" + chat_id + "\'"
                    cursor.execute(stmt)
                    chat = cursor.fetchone()

                # print("new chat id: " + chat_id)
                stmt = "INSERT INTO chats VALUES (\'" + user + \
                       "\', \'" + match + "\', \'" + chat_id + "\');"
                cursor.execute(stmt)
                connect.commit()

    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)
        print("Data base connection failed", file=stderr)
        return ["unknown (database connection failed)", "unknown"]


# Takes chat_id, message content, and sender (net_id), and adds to
# database
def send_chat(chat_id, sender, message):
    try:
        # connect to database
        with psycopg2.connect(host="ec2-3-217-113-25.compute-1.amazonaws.com",
                              database="dd4c5lulvqtkld",
                              user="fpzzhwdkkymqrr",
                              password="b87ef0b3ae33d79f063d25d7ec8dde6871405d7d85b67ddff7f1ddaec3d00361") as connect:
            with connect.cursor() as cursor:
                now = str(datetime.now())

                stmt = "INSERT INTO messages VALUES (\'" + chat_id + "\', \'" + \
                       sender + "\', \'" + message + "\', \'" + now + "\');"
                cursor.execute(stmt)
                connect.commit()

    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)
        print("Data base connection failed", file=stderr)
        return ["unknown (database connection failed)", "unknown"]


# get all message history from a given chat_id
def get_messages(chat_id):
    try:
        # connect to database
        with psycopg2.connect(host="ec2-3-217-113-25.compute-1.amazonaws.com",
                              database="dd4c5lulvqtkld",
                              user="fpzzhwdkkymqrr",
                              password="b87ef0b3ae33d79f063d25d7ec8dde6871405d7d85b67ddff7f1ddaec3d00361") as connect:
            with connect.cursor() as cursor:
                stmt = "SELECT * FROM messages WHERE chat_id=\'" + \
                       chat_id + "\' ORDER BY datetime DESC;"
                cursor.execute(stmt)
                msgs = cursor.fetchone()
                chat_history = ()
                while msgs is not None:
                    user = get_account_details(str(msgs[1]))[0]
                    chat_history += ((user, str(msgs[2]),
                                      str(msgs[3])),)
                    msgs = cursor.fetchone()

                return chat_history

    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)
        print("Data base connection failed", file=stderr)
        return ["unknown (database connection failed)", "unknown"]


# unit test
def main():
    myself = 'collado'
    chats = get_all_chats(myself)
    print(chats)
    id1 = get_chat_id(myself, chats[0])
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
