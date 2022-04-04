# --------------------------------------------------------------------
# chat.py
# --------------------------------------------------------------------
from cgitb import reset
import random
from sys import stderr
import psycopg2

DATABASE_URL = 'file:TigerFriend.sqlite?mode=ro'

# --------------------------------------------------------------------

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
                    print("No match username found", file=stderr)
                    return "No match username found"
                match = str(match[0])
                print("Match's net_id: " + match)
                
                stmt = "SELECT * FROM chats WHERE net_id1=\'" + user + "\' OR net_id2=\'" + user + "\'"
                cursor.execute(stmt)
                chats = cursor.fetchone()
                chat_id = None
                while chats is not None:
                    print("Chat_id found: " + str(chats[2]))
                    if str(chats[0]) == match or str(chats[1]) == match:
                        print("Match!")
                        chat_id = str(chats[2])
                        break
                    chats = cursor.fetchone()
                if chat_id is None:
                    print("making new chat")
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
                
                print("new chat id: " + chat_id)
                stmt = "INSERT INTO chats VALUES (\'" + user + "\', \'" + match + "\', \'" + chat_id + "\');"
                cursor.execute(stmt)
                connect.commit()

    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)
        print("Data base connection failed", file=stderr)
        return ["unknown (database connection failed)", "unknown"]

# Takes chat_id, message content, and sender (net_id), and adds to 
# database
def send_chat(chat_id, message, sender):
    try:
        # connect to database
        with psycopg2.connect(host="ec2-3-217-113-25.compute-1.amazonaws.com",
                              database="dd4c5lulvqtkld",
                              user="fpzzhwdkkymqrr",
                              password="b87ef0b3ae33d79f063d25d7ec8dde6871405d7d85b67ddff7f1ddaec3d00361") as connect:
            with connect.cursor() as cursor:
                return 'NOT DONE YET'

    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)
        print("Data base connection failed", file=stderr)
        return ["unknown (database connection failed)", "unknown"]

# unit test
def main():
    print(get_chat_id('collado', 'haha371'))

# ----------------------------------------------------------------------

if __name__ == '__main__':
    main()
