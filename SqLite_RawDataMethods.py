from sys import stderr, exit
from contextlib import closing
from sqlite3 import connect

DATABASE_URL = 'file:TigerFriend.sqlite?mode=ro'

def accountCreation(net_id, year, maj):
    try:
        with connect(DATABASE_URL, isolation_level=None,
        uri=True) as connection:

            with closing(connection.cursor()) as cursor:
                stmt = "INSERT INTO RawData (net_id, class_year, major)"
                stmt += "VALUES (?, ?, ?)"
                cursor.execute(stmt, (net_id, year, maj))

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

def accountPopulation(net_id, user, bio, q1, q2):
    try:
        with connect(DATABASE_URL, isolation_level=None,
        uri=True) as connection:
            with closing(connection.cursor()) as cursor:
                stmt = "UPDATE RawData username = ?, "
                stmt += "bio_string = ?, "
                stmt += "survery_q1_response = ?, "
                stmt += "survery_q1_response = ?, "
                stmt += "WHERE net_id = ?"
                cursor.execute(stmt, (net_id, user, bio, q1, q2))
    
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

def updateBio(net_id, bio):
    try:
        with connect(DATABASE_URL, isolation_level=None,
        uri=True) as connection:
            with closing(connection.cursor()) as cursor:
                stmt = "UPDATE RawData bio_string = ?"
                stmt += "WHERE net_id = ?"
                cursor.execute(stmt, (bio, net_id))
    
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

def updateUsername(net_id, user):
    try:
        with connect(DATABASE_URL, isolation_level=None,
        uri=True) as connection:
            with closing(connection.cursor()) as cursor:
                stmt = "UPDATE RawData username = ?"
                stmt += "WHERE net_id = ?"
                cursor.execute(stmt, (user, net_id))
    
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)
