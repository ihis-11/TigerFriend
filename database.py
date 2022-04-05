#!/usr/bin/env python

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Account(Base):
    __tablename__ = 'account'
    net_id = Column(String, primary_key=True)
    username = Column(String)
    class_year = Column(String)
    major = Column(String)
    bio_string = Column(String)
    res_college = Column(String)
