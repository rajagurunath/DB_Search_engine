from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from whooshalchemy import IndexService
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Text, DateTime,BOOLEAN
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker

import sqlite3
import flask_whooshalchemy as wa 
import os
os.getcwd()
DATABASE_URL=os.getcwd()
config = {"WHOOSH_BASE": os.path.join(os.getcwd(),"Database"),
         "DATABASE_URL": os.path.join(os.getcwd(),"Database"),
         "dbname":'user'}

# app=Flask(__name__)
# #ss=sqlite3.connect('srch.db')
# app.config['SQLALCHEMY_DATABASE_URL']='sqlite3://F:\searchEngine\DB_Search_engine\srch.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
# app.config['DEBUG']=True
# app.config['WHOOSH_BASE']='whoosh_try'
# db=SQLAlchemy(app)
# class Srch(db.Model):
#     __searchable__=['name','desc']
#     id=db.Column(db.Integer,primary_key=True)
#     name=db.Column(db.String(30))
#     desc=db.Column(db.String(100))
#     db.make_connector(app.config['SQLALCHEMY_DATABASE_URL'])

# wa.whoosh_index(app,Srch)




# r1=Srch(name='ggg',desc='i am grook')
# db.session.add(r1)
# db.session.commit()



class Agent(Base):
   __tablename__ = 'agent'
   __searchable__ = []  # these fields will be indexed by whoosh

   id = Column(Integer, primary_key=True)
   category=Column(Text)
   name=Column(Text)
   location=Column(Text)
   whatsapp=Column(Integer)
   mobile_number = Column(Integer)
   email=Column(Text)
   always=Column(BOOLEAN)
   def dataframe():
       return 
   def __repr__(self):
       return '{0}(title={1})'.format(self.__class__.__name__, self.full_name)
def sqldb(dbname):
    Base = declarative_base()
    if dbname=='user':
        class UserDB(Base):
            __tablename__ = 'usertable'
            __searchable__ = ['name']  # these fields will be indexed by whoosh
            id = Column(Integer, primary_key=True)
            name = Column(Text)
            mobile_number = Column(Integer)
            email=Column(Text)
            date=Column(DateTime)
            comments=Column(Text)
            def __repr__(self):
                return '{0}(title={1})'.format(dbname, self.full_name)

        db=UserDB
    if dbname=='agent':
        class AgentDB(Base):
            __tablename__ = 'agenttable'
            __searchable__ = ['name','location']  # these fields will be indexed by whoosh

            id = Column(Integer, primary_key=True)
            category=Column(Text)
            name=Column(Text)
            location=Column(Text)
            whatsapp=Column(Integer)
            mobile_number = Column(Integer)
            email=Column(Text)
            always=Column(BOOLEAN)
            def __repr__(self):
                #return '{0}(title={1})'.format(self.__class__.__name__, self.full_name)
                return [self.name,self.location]
        db=AgentDB
    return db



class dbUtils(object):
    def __init__(self,config,session,engine):
        self.config=config
        #self.engine = create_engine(r'sqlite:///{}\{}.db'.format(self.config['DATABASE_URL'],self.config['dbname']))
        #self.engine = create_engine(r'sqlite:///{}.db'.format(self.config['dbname']))
        #self.engine=create_engine('sqlite:///:memory:user.db')
        #Session = sessionmaker(bind=self.engine)
        #self.session = Session()
        #Base = declarative_base()
        self.engine=engine
        self.session=session
        self.index_service = IndexService(config=self.config, session=self.session)
        if config['dbname']=='user':
            self.db=UserDB
        elif config['dbname']=='agent':
            self.db=AgentDB
        self.register_db()
    def register_db(self):
        Base.metadata.create_all(self.engine)
        self.index_service.register_class(self.db)
    def add_documents(self,dict_):
        try:
            print('add')
            ins=self.db(**dict_)
            self.session.add(ins)
            self.session.commit()
            #self.session.rollback()
            #self.session.close()
        except Exception as e:
            print('add exce',e)
            self.session.rollback()
            self.session.close()
        #    self.close()
    def search_index(self,query):
        return list(self.db.search_query(query))
    def dataframe(self,dbname):
        
        path=self.self.config['DATABASE_URL']+self.config['dbname']+'.db'
        conn=sqlite3.connect(path)
        df=pd.read_sql('select * from {}'.format(dbname),conn)
        conn.close()
        return df
    def export_csv(self,csvfilename):
        return self.dataframe(self.config['dname']).to_csv(csvfilename,index=False)

#Base.metadata.create_all(engine)



#FileIndex(FileStorage('/tmp/whoosh/BlogPost'), 'MAIN')

m = BlogPost(title=u'My cool title', content=u'This is the first post.')
session.add(m); session.commit()

list(BlogPost.search_query(u'cool'))
#[BlogPost(title=My cool title)]s
list(BlogPost.search_query(u'first'))
#[BlogPost(title=My cool title)]

list(BlogPost.search_query(u'first').filter(BlogPost.id >= 0))
import pandas as pd
path=r'F:\searchEngine\DB_Search_engine\BlogPost.db '
conn=sqlite3.connect(path)

engine = create_engine('sqlite:///userDb.db')
Session = sessionmaker(bind=engine)
session = Session()


db1=dbUtils(config,session,engine)
user_dict=dict(name='guru1',mobile_number=9444532122,email='guru@gmail.com',date=datetime.strptime('29/09/2018','%d/%m/%Y'),comments='very good')
db1.add_documents(user_dict)
db1.config
engine
ce=create_engine(r'sqlite:///F:\searchEngine\DB_Search_engine\Database\user.db')

engine1 = create_engine('sqlite:///:agent.db')
Session = sessionmaker(bind=engine1)
session = Session()


config['dbname']='agent'
db2=dbUtils(config,session)
agent_dict=dict(category='travel',name='guru',location='pammal',whatsapp=94444526172,
mobile_number = 874308230823,email='qba@gmail.com',always=True)

db2.add_documents(agent_dict)
db2.config
db2.engine
ce=create_engine(r'sqlite:///F:\searchEngine\DB_Search_engine\Database\user.db',extend



class BlogPost(Base):
   __tablename__ = 'blogpost'
   __searchable__ = ['title', 'content']  # these fields will be indexed by whoosh
   id = Column(Integer, primary_key=True)
   title = Column(Text)
   content = Column(Text)

   def __repr__(self):
       return '{0}(title={1})'.format(self.__class__.__name__, self.title)

engine = create_engine('sqlite:///userdb.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

u=dbUtils(config,session,engine)
u.add_documents(user_dict)

engine = create_engine('sqlite:///agentdb.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
config['dbname']='agent'
a=dbUtils(config,session,engine)
a.add_documents(agent_dict)



Base.metadata.create_all(engine)
index_service = IndexService(config=config, session=session)
index_service.register_class(BlogPost)
m = BlogPost(title=u'My machines are dunp', content=u'learn databases quickly This is the first post.')
session.add(m);
session.commit()
import pandas as pd
path=r'F:\searchEngine\DB_Search_engine\BlogPost.db'
conn=sqlite3.connect(path)
pd.read_sql('select * from blogpost',conn)

class UserDB(Base):
    __tablename__ = 'usertable'
    __searchable__ = ['name']  # these fields will be indexed by whoosh
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    mobile_number = Column(Integer)
    email=Column(Text)
    date=Column(DateTime)
    comments=Column(Text)
    def __repr__(self):
        return '{0}(title={1})'.format(dbname, self.full_name)

engine = create_engine('sqlite:///userdb.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

Base.metadata.create_all(engine)
index_service = IndexService(config=config, session=session)

index_service.register_class(UserDB)
u=UserDB(**user_dict)
#m = BlogPost(title=u'My machines are dunp', content=u'learn databases quickly This is the first post.')
session.add(u);
session.commit()
import pandas as pd
path=r'F:\searchEngine\DB_Search_engine\userdb.db'
conn=sqlite3.connect(path)
pd.read_sql('select * from usertable',conn)

class AgentDB(Base):
    __tablename__ = 'agenttable'
    __searchable__ = ['name','location']  # these fields will be indexed by whoosh

    id = Column(Integer, primary_key=True)
    category=Column(Text)
    name=Column(Text)
    location=Column(Text)
    whatsapp=Column(Integer)
    mobile_number = Column(Integer)
    email=Column(Text)
    always=Column(BOOLEAN)
    def __repr__(self):
        #return '{0}(title={1})'.format(self.__class__.__name__, self.full_name)
        return [self.name,self.location]




