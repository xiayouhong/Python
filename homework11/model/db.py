# -*- coding: utf-8 -*-
# @Time    : 2020/5/18 14:04
# @Author  : xyh
from sqlalchemy import Column, String,Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class student(Base):
    __tablename__ = 'student'
    id = Column(String(20), primary_key=True)
    name = Column(String(30))
    password = Column(String(20))
    

class subject(Base):
    __tablename__ = 'subject'
    id = Column(String(20), primary_key = True)
    sub = Column(String(30))
    time = Column(String(30))
    selected = Column(Integer)


class timetable(Base):
    __tablename__ = 'timetable'
    id = Column(String(20), primary_key=True)
    mon = Column(String(30))
    tue = Column(String(30))
    wed = Column(String(30))
    thu = Column(String(30))
    fri = Column(String(30))
    sat = Column(String(30))
    sun = Column(String(30))


engine = create_engine('mysql+mysqlconnector://root:1234a@localhost:3306/test')
DBSession = sessionmaker(bind=engine)
session = DBSession()



