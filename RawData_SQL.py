from sys import stderr, exit
import psycopg2

def account_creation(net_id, year, maj):
    try:
        with psycopg2.connect(host = "ec2-3-229-161-70.compute-1.amazonaws.com",
                                   database = "d2fdvi8f5tvpvo",
                                   user = "yfdafrxedkbxza",
                                   password = "3768ffff6c40b7ca1d4274e6d428b9adbd6c5d8becd30b6c479236de989a8f1e") as connect:
            if connect is not None:
                print("CONNECTED TO POSTGRESQL")
            else: 
                print(connect)
                raise Exception("Connect was null")
            with connect.cursor() as cursor:
                stmt = "INSERT INTO account (net_id, class_year, major) VALUES (\'" + net_id + "\', \'" + year + "\', \'" + maj + "\');"
                print(stmt)
                cursor.execute(stmt)

                connect.commit()
                count = cursor.rowcount
                print(count, "Record inserted successfully into account")

    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)
        print("Account creation failed", file = stderr)
    #finally:
    #   if connect is not None:
    #       if(connect):
    #           cursor.close()
    #           connect.close()

def account_population(net_id, user, bio, q1, q2):
    try:
        with psycopg2.connect(host = "ec2-3-229-161-70.compute-1.amazonaws.com",
                                   database = "d2fdvi8f5tvpvo",
                                   user = "yfdafrxedkbxza",
                                   password = "3768ffff6c40b7ca1d4274e6d428b9adbd6c5d8becd30b6c479236de989a8f1e") as connect:

            with connect.cursor() as cursor:
                stmt = "UPDATE Raccount SET username = (%s), "
                stmt += "bio_string = (%s), "
                stmt += "survery_q1_response = (%s), "
                stmt += "survery_q1_response = (%s), "
                stmt += "WHERE net_id = (%s)"
                cursor.execute(stmt, (user, bio, q1, q2, net_id))

                connect.commit()
                count = cursor.rowcount
                print(count, "Record inserted successfully into account")

    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)
        print("Account population failed", file=stderr)

def update_bio(net_id, bio):
    try:
        with psycopg2.connect(host = "ec2-3-229-161-70.compute-1.amazonaws.com",
                                   database = "d2fdvi8f5tvpvo",
                                   user = "yfdafrxedkbxza",
                                   password = "3768ffff6c40b7ca1d4274e6d428b9adbd6c5d8becd30b6c479236de989a8f1e") as connect:

            with connect.cursor() as cursor:
                stmt = "UPDATE account SET bio_string = (%s)"
                stmt += "WHERE net_id = (%s)"
                cursor.execute(stmt, (bio, net_id))

                connect.commit()
                count = cursor.rowcount
                print(count, "Record inserted successfully into account")
    
    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)
        print("Update bio failed", file=stderr)

def update_username(net_id, user):
    try:
        with psycopg2.connect(host = "ec2-3-229-161-70.compute-1.amazonaws.com",
                                   database = "d2fdvi8f5tvpvo",
                                   user = "yfdafrxedkbxza",
                                   password = "3768ffff6c40b7ca1d4274e6d428b9adbd6c5d8becd30b6c479236de989a8f1e") as connect:
            with connect.cursor() as cursor:
                stmt = "UPDATE account SET username = (%s)"
                stmt += "WHERE net_id = (%s)"
                cursor.execute(stmt, (user, net_id))
    
    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)
        print("Update username failed", file=stderr)

def get_user_data(net_id): # returns year and major
    try:
        with psycopg2.connect(host = "ec2-3-229-161-70.compute-1.amazonaws.com",
                                   database = "d2fdvi8f5tvpvo",
                                   user = "yfdafrxedkbxza",
                                   password = "3768ffff6c40b7ca1d4274e6d428b9adbd6c5d8becd30b6c479236de989a8f1e") as connect:
            with connect.cursor() as cursor:
                stmt = "SELECT class_year, major FROM account WHERE net_id = \'" + net_id + "\'"
                print(stmt)
                cursor.execute(stmt)

                row = cursor.fetchone()
                if row is None:
                    return "unknown (" + net_id + " USER NOT FOUND)"
                else:
                    return [row[0], row[1]]
    
    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)
        print("Data base connection failed", file=stderr)
        return ["unknown (database connection failed)", "unknown"]