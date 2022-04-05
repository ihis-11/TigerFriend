from sys import stderr, exit
from turtle import update
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Account


DATABASE_URL = 'postgresql://fpzzhwdkkymqrr:b87ef0b3ae33d79f063d25d7ec8dde6871405d7d85b67ddff7f1ddaec3d00361@ec2-3-217-113-25.compute-1.amazonaws.com:5432/dd4c5lulvqtkld'

def api_account_creation(net_id, year, maj, res, user, bio):
    try:
        engine = create_engine(DATABASE_URL)
         
        Session = sessionmaker(bind=engine)
        session = Session()

        newAccount = Account(net_id = net_id, 
                                username = user, 
                                class_year = year, 
                                major = maj, 
                                bio_string = bio, 
                                res_college = res)

        session.add(newAccount)
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
        if user == []:
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
        if user == []:
            return ["unknown (" + net_id + " not found)", "?"]
        return[user[0].class_year, user[0].major]
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
        if user == []:
            return None
        return[user[0].username, user[0].bio_string]

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
