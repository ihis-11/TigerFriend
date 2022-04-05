#!/usr/bin/env python

from sys import stderr
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Reports

DATABASE_URL = 'postgresql://fpzzhwdkkymqrr:b87ef0b3ae33d79f063d25d7ec8dde6871405d7d85b67ddff7f1ddaec3d00361@ec2-3-217-113-25.compute-1.amazonaws.com:5432/dd4c5lulvqtkld'

# Report user with given reporter/reported net_id and type and comment
def report_user(reporter, reported, rep_type, comment):
    try:
        engine = create_engine(DATABASE_URL)
         
        Session = sessionmaker(bind=engine)
        session = Session()

        newReport = Reports(reporter_net_id = reporter,
                            reported_net_id = reported,
                            type_of_report = rep_type,
                            report_comment = comment)

        session.add(newReport)
        session.commit()
                        
        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)