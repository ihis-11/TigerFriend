from sys import stderr, exit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URI = 'postgres://fpzzhwdkkymqrr:b87ef0b3ae33d79f063d25d7ec8dde6871405d7d85b67ddff7f1ddaec3d00361@ec2-3-217-113-25.compute-1.amazonaws.com:5432/dd4c5lulvqtkld'

def api_account_creation(net_id, year, major, res_college, username, bio):
