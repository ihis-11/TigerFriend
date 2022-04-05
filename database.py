#!/usr/bin/env python

from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

class Account(Base):
    __tablename__ = 'account'
    net_id = Column(String, primary_key=True)
    username = Column(String)
    class_year = Column(String)
    major = Column(String)
    bio_string = Column(String)
    res_college = Column(String)

class RawData(Base):
    __tablename__ = 'rawdata'
    net_id = Column(String, primary_key=True)
    q1_response = Column(Integer)
    q2_response = Column(Integer)
    q3_response = Column(Integer)
    q4_response = Column(Integer)
    q5_response = Column(Integer)
    q6_response = Column(Integer)
    q7_response = Column(Integer)
    q8_response = Column(Integer)
    q9_response = Column(Integer)
    q10_response = Column(Integer)
    q11_response = Column(Integer)
    q12_response = Column(Integer)
    q13_response = Column(Integer)
    q14_response = Column(Integer)
    q15_response = Column(Integer)
    q16_response = Column(Integer)
    q17_response = Column(Integer)
    q18_response = Column(Integer)
    q19_response = Column(Integer)
    q20_response = Column(Integer)
    q21_response = Column(Integer)
    q22_response = Column(Integer)
    q23_response = Column(Integer)
    q24_response = Column(Integer)

# class MatchScores(Base):
#     __tablename__  = 'matchscores'
#     net_id1 = Column(String)
#     net_id2 = Column(String)
#     overall_score = Column(Integer)
#     academic_score = Column(Integer)
#     ec_score = Column(Integer)
#     personality_score = Column(Integer)
#     opinion_score = Column(Integer)

class Chats(Base):
    __tablename__ = 'chats'
    net_id1 = Column(String)
    net_id2 = Column(String)
    chat_id = Column(String, primary_key=True)

class Messages(Base):
    __tablename__ = 'messages'
    chat_id = Column(String)
    sender_id = Column(String)
    message_content = Column(String)
    date_time = Column(DateTime, primary_key=True)

# class Reports(Base):
#     __tablename__ = 'reports'
#     reporter_net_id = Column(String)
#     reported_net_id = Column(String)
#     type_of_report = Column(Integer)
#     report_comment = Column(String)

class Administrators(Base):
    __tablename__ = 'administrators'
    net_id = Column(String, primary_key=True)

class Survey(Base):
    __tablename__ = 'survey'
    q_num = Column(Integer, primary_key=True)
    question = Column(String)
    q_type = Column(Integer)
    answer1 = Column(String)
    answer2 = Column(String)
    answer3 = Column(String)
    answer4 = Column(String)
    answer5 = Column(String)