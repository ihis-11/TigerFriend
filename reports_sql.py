#!/usr/bin/env python

from sys import stderr
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Reports

DATABASE_URL = configs.DATABASE_URL


# Report user with given reporter/reported net_id and type and comment
def report_user(reporter, reported, rep_type, comment):
    try:
        engine = create_engine(DATABASE_URL)

        Session = sessionmaker(bind=engine)
        session = Session()

        new_report = Reports(reporter_net_id=reporter,
                             reported_net_id=reported,
                             type_of_report=rep_type,
                             report_comment=comment)

        session.add(new_report)
        session.commit()

        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)
