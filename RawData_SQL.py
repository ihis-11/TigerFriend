from sys import stderr
import psycopg2


def api_account_creation(net_id, year, major, res_college, username, bio):
    try:
        with psycopg2.connect(host="ec2-3-217-113-25.compute-1.amazonaws.com",
                              database="dd4c5lulvqtkld",
                              user="fpzzhwdkkymqrr",
                              password="b87ef0b3ae33d79f063d25d7ec8dde6871405d7d85b67ddff7f1ddaec3d00361") as connect:
            if connect is not None:
                print("CONNECTED TO POSTGRESQL")
            else:
                print(connect)
                raise Exception("Connect was null")
            with connect.cursor() as cursor:
                stmt = "INSERT INTO account (net_id, class_year, major, res_college, username, bio_string) VALUES \
                (\'" + net_id + "\', \'" + year + "\', \'" + major + "\', \'" + res_college + "\', %s, %s);"
                print(stmt)
                cursor.execute(stmt, (username, bio))

                connect.commit()
                count = cursor.rowcount
                print(count, "Record inserted successfully into account")
    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)
        print("Account creation failed", file=stderr)


def update_bio(net_id, bio):
    try:
        with psycopg2.connect(host="ec2-3-217-113-25.compute-1.amazonaws.com",
                              database="dd4c5lulvqtkld",
                              user="fpzzhwdkkymqrr",
                              password="b87ef0b3ae33d79f063d25d7ec8dde6871405d7d85b67ddff7f1ddaec3d00361") as connect:

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
        with psycopg2.connect(host="ec2-3-217-113-25.compute-1.amazonaws.com",
                              database="dd4c5lulvqtkld",
                              user="fpzzhwdkkymqrr",
                              password="b87ef0b3ae33d79f063d25d7ec8dde6871405d7d85b67ddff7f1ddaec3d00361") as connect:
            with connect.cursor() as cursor:
                stmt = "UPDATE account SET username = (%s)"
                stmt += "WHERE net_id = (%s)"
                cursor.execute(stmt, (user, net_id))

    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)
        print("Update username failed", file=stderr)


def get_user_data(net_id):  # returns year and major
    try:
        with psycopg2.connect(host="ec2-3-217-113-25.compute-1.amazonaws.com",
                              database="dd4c5lulvqtkld",
                              user="fpzzhwdkkymqrr",
                              password="b87ef0b3ae33d79f063d25d7ec8dde6871405d7d85b67ddff7f1ddaec3d00361") as connect:
            with connect.cursor() as cursor:
                stmt = "SELECT class_year, major FROM account WHERE net_id=\'" + net_id + "\'"
                print(stmt)
                cursor.execute(stmt, net_id)

                row = cursor.fetchone()
                if row is None:
                    return ["unknown (" + net_id + " not found)", "?"]
                else:
                    return [row[0], row[1]]

    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)
        print("Data base connection failed", file=stderr)
        return ["unknown (database connection failed)", "unknown"]

def get_account_details(net_id):  # returns user and bio, None if account doesn't exist
    try:
        with psycopg2.connect(host="ec2-3-217-113-25.compute-1.amazonaws.com",
                              database="dd4c5lulvqtkld",
                              user="fpzzhwdkkymqrr",
                              password="b87ef0b3ae33d79f063d25d7ec8dde6871405d7d85b67ddff7f1ddaec3d00361") as connect:
            with connect.cursor() as cursor:
                stmt = "SELECT username, bio_string FROM account WHERE net_id=\'" + net_id + "\'"
                cursor.execute(stmt)
                row = cursor.fetchone()
                if row is None:
                    return None
                else:
                    return [row[0], row[1]]

    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)
        print("Data base connection failed", file=stderr)
        return ["unknown (database connection failed)", "unknown"]

# Method for deleting rows in matchscores, account, and rawdata
def delete():  # returns user and bio, None if account doesn't exist
    try:
        with psycopg2.connect(host="ec2-3-217-113-25.compute-1.amazonaws.com",
                              database="dd4c5lulvqtkld",
                              user="fpzzhwdkkymqrr",
                              password="b87ef0b3ae33d79f063d25d7ec8dde6871405d7d85b67ddff7f1ddaec3d00361") as connect:
            with connect.cursor() as cursor:
                # HARD CODE IN NET_ID YOU WANT TO DELETE
                ID = "NET_ID" # REPLACE NET_ID HERE WITH WHAT YOU WANT TO REMOVE - then run "python RawData_SQL.py"
                stmt = "DELETE FROM matchscores WHERE net_id1=\'" + ID + "\' OR net_id2=\'" + ID + "\'"
                cursor.execute(stmt)
                connect.commit()

                stmt = "DELETE FROM account WHERE net_id=\'" + ID + "\'"
                cursor.execute(stmt)
                connect.commit()

                stmt = "DELETE FROM rawdata WHERE net_id=\'" + ID + "\'"
                cursor.execute(stmt)
                connect.commit()

    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)
        print("Data base connection failed", file=stderr)
        return ["unknown (database connection failed)", "unknown"]

# ----------------------------------------------------------------------

if __name__ == '__main__':
    delete()
