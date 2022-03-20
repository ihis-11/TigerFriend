from sys import stderr
import psycopg2

try:
    #connect to db hopefully
    connect = psycopg2.connect(
        host = "localhost",
        database = "TigerFriend",
        user = "postgres",
        password = "RNCHL")
    print("It worked?")
    cursor = connect.cursor()
    print("PostgreSQL server information")
    print(connect.get_dsn_parameters(), "\n")
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

except Exception as ex:
    print("Error connecting to PostgreSQL", stderr)
finally:
    if(connect):
        cursor.close()
        connect.close()
