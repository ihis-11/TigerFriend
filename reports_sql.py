#!/usr/bin/env python

from sys import stderr
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database import Reports
import configs
from datetime import datetime

DATABASE_URL = configs.DATABASE_URL


# Report user with given reporter/reported net_id and type and comment
def report_user(reporter, reported, rep_type, rep_comment):
    try:
        engine = create_engine(DATABASE_URL)

        Session = sessionmaker(bind=engine)
        session = Session()

        last_id = (session.query(Reports)
                    .order_by(desc(Reports.date_time))
                    .first())

        new_id = int(last_id.report_id) + 1
        now = str(datetime.now())

        new_report = Reports(report_id=new_id,
                             reporter_net_id=reporter,
                             reported_net_id=reported,
                             type=rep_type,
                             comment=rep_comment,
                             date_time=now)

        session.add(new_report)
        session.commit()

        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

def get_all_reports():
    try:
        engine = create_engine(DATABASE_URL)

        Session = sessionmaker(bind=engine)
        session = Session()

        reports = (session.query(Reports.report_id, Reports.reported_net_id, Reports.type, Reports.comment)
                    .all())
                    
        return reports

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)