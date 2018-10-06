from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from whooshalchemy import IndexService
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Text, DateTime,BOOLEAN,Boolean
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
import pandas as pd
import sqlite3
#import flask_whooshalchemy as wa 
import os

config = {"WHOOSH_BASE": os.path.join(os.getcwd(),"Database")}
Base = declarative_base()

class UserDB(Base):
    __table_args__ = {'extend_existing': True} 

    __tablename__ = 'usertable'
    __searchable__ = ['name']  # these fields will be indexed by whoosh
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    mobile_number = Column(Integer)
    email=Column(Text)
    date=Column(DateTime)
    comments=Column(Text)
    def __repr__(self):
        #return '({})'.format(self.name)
        return '{0}(title={1})'.format(self.__class__.__name__, self.name)

class AgentDB(Base):
    __table_args__ = {'extend_existing': True} 

    __tablename__ = 'agenttable'
    __searchable__ = ['name','location']  # these fields will be indexed by whoosh
    id = Column(Integer, primary_key=True)
    category=Column(Text)
    name=Column(Text)
    location=Column(Text)
    whatsapp=Column(Integer)
    mobile_number = Column(Integer)
    email=Column(Text)
    always=Column(Boolean)
    def __repr__(self):
        return '{0}(title={1},location={2})'.format(self.__class__.__name__, self.name,self.location)
        #return '({},{})'.format(self.name,self.location)

user_dict=dict(name='guru',mobile_number=9444532122,email='guru@gmail.com',date=datetime.strptime('29/09/2018','%d/%m/%Y'),comments='very good')
agent_dict=dict(category='travel',name='guru',location='pammal',whatsapp=94444526172,
mobile_number = 874308230823,email='qba@gmail.com',always=True)

def add_documents(dbname,update_dict):
    """
    dbname='userdb' or agentdb
    """
    print(dbname)
    engine = create_engine('sqlite:///{}.db'.format(dbname))
    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)
    index_service = IndexService(config=config, session=session)
    if dbname=='userdb':
        index_service.register_class(UserDB)
        add=UserDB(**update_dict)
    elif dbname=='agentdb':
        print(dbname,'agent')
        index_service.register_class(AgentDB)
        add=AgentDB(**update_dict)
    #m = BlogPost(title=u'My machines are dunp', content=u'learn databases quickly This is the first post.')

    session.add(add)
    session.commit()
def srch_documents(dbname,query):
    """
    dbname='userdb' or agentdb
    """
    user_schema=['id','name','mobile_number','email','date','comments']
    agent_schema=['id','category','name','location','whatsapp','mobile_number','email','always']
    print(dbname)
    engine = create_engine('sqlite:///{}.db'.format(dbname))
    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)
    index_service = IndexService(config=config, session=session)
    res_list=[]
    if dbname=='userdb':
        index_service.register_class(UserDB)            
        db=UserDB
        
        for cl in list(db.search_query(query)):
            res=dict()
            for col in user_schema:
                res[col]=cl.__dict__[col]
            res_list.append(res)
        # res['id']=UserDB.__dict__['id']
        # res['name']=UserDB.__dict__['name']
        # res['mobile_number']=UserDB.__dict__['mobile_number']
        # res['email']=UserDB.__dict__['email']
        # res['date']=UserDB.__dict__['date']
        # res['comments']=UserDB.__dict__['comments']
        #add=UserDB(**update_dict)
    elif dbname=='agentdb':
        index_service.register_class(AgentDB)
        db=AgentDB
        for cl in list(db.search_query(query)):
            res=dict()
            for col in agent_schema:
                res[col]=cl.__dict__[col]
            res_list.append(res)
    return res_list
    # session.add(add)
    # session.commit()

def search_documents(query,dbname,engine,session,index_service):
    print(locals())
    print(locals()['session'])
    # global session
    # global engine
    # global index_service
    #engine = create_engine('sqlite:///{}.db'.format(dbname))
    print(engine)
    if dbname=='userdb':
        db=UserDB
    if dbname=='agentdb':
        db=AgentDB
    print(db)
    #Session = sessionmaker(bind=engine)
    #session = Session()
    
    #Base.metadata.create_all(engine)
    #index_service = IndexService(config=config, session=session)

    #index_service.register_class(db)
    return list(UserDB.search_query(query))
if __name__=='__main__':
    add_documents('userdb',user_dict)
    add_documents('agentdb',agent_dict)
    query=input('Enter the query')
    print(srch_documents('agentdb',query))
    query=input('Enter the query')
    print(srch_documents('userdb',query))
# engine = create_engine('sqlite:///userdb.db')
# Session = sessionmaker(bind=engine)
# session = Session()

# Base.metadata.create_all(engine)
# index_service = IndexService(config=config, session=session)

# index_service.register_class(UserDB)
# list(UserDB.search_query('lasttry'))
#search_documents('lasttry','userdb',engine,session,index_service)

# u=UserDB(**user_dict)
# #m = BlogPost(title=u'My machines are dunp', content=u'learn databases quickly This is the first post.')

# session.add(u)
# session.commit()


# engine = create_engine('sqlite:///agentdb.db')
# Session = sessionmaker(bind=engine)
# session = Session()

# Base.metadata.create_all(engine)
# index_service = IndexService(config=config, session=session)
# index_service.register_class(AgentDB)

# |#m = BlogPost(title=u'My machines are dunp', content=u'learn databases quickly This is the first post.')
# a=AgentDB(**agent_dict)
# session.add(a)
# session.commit()

# list(AgentDB.search_query('guru'))
# list(UserDB.search_query('lasttry'))
# globals()