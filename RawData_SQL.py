from sys import stderr, exit
import psycopg2

def account_creation(net_id, year, maj):
    try:
        connect = psycopg2.connect(host = "10.8.53.63",
                                   database = "TigerFriend",
                                   user = "postgres",
                                   password = "RNCHL")

        cursor = connect.cursor()
        stmt = "INSERT INTO RawData (net_id, class_year, major) VALUE"
        stmt += "((%s), (%s), (%s))"
        cursor.execute(stmt, (net_id, year, maj))

        connect.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into RawData")

    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)
        exit(1)
    finally:
        if(connect):
            cursor.close()
            connect.close()

def account_population(net_id, user, bio, q1, q2):
    try:
        connect = psycopg2.connect(host = "10.8.53.63",
                                   database = "TigerFriend",
                                   user = "postgres",
                                   password = "RNCHL")

        cursor = connect.cursor()
        stmt = "UPDATE RawData SET username = (%s), "
        stmt += "bio_string = (%s), "
        stmt += "survery_q1_response = (%s), "
        stmt += "survery_q1_response = (%s), "
        stmt += "WHERE net_id = (%s)"
        cursor.execute(stmt, (user, bio, q1, q2, net_id))

        connect.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into RawData")

    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)
        exit(1)
    finally:
        if(connect):
            cursor.close()
            connect.close()

def update_bio(net_id, bio):
    try:
        connect = psycopg2.connect(host = "10.8.53.63",
                                   database = "TigerFriend",
                                   user = "postgres",
                                   password = "RNCHL")

        cursor = connect.cursor()
        stmt = "UPDATE RawData SET bio_string = (%s)"
        stmt += "WHERE net_id = (%s)"
        cursor.execute(stmt, (bio, net_id))

        connect.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into RawData")
    
    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)
        exit(1)
    finally:
        if(connect):
            cursor.close()
            connect.close()

def update_username(net_id, user):
    try:
        connect = psycopg2.connect(host = "10.8.53.63",
                                   database = "TigerFriend",
                                   user = "postgres",
                                   password = "RNCHL")
        cursor = connect.cursor()
        stmt = "UPDATE RawData SET username = (%s)"
        stmt += "WHERE net_id = (%s)"
        cursor.execute(stmt, (user, net_id))
    
    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)
        exit(1)
    finally:
        if(connect):
            cursor.close()
            connect.close()