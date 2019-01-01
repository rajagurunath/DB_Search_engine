from mongoengine import *
from datetime import datetime
import json
import pandas as pd

user_schema=['id','name','mobile_number','email','date','comments']
agent_schema=['id','category','name','location','whatsapp','mobile_number','email','always']


class User(Document):
    name = StringField()
    mobile_number=IntField()
    email=StringField()
    date=DateTimeField()
    comments=StringField()
    meta = {'indexes': [
        {'fields': ['$name',],
         'default_language': 'english',
         'weights': {'name': 5,}
        }
    ]}


class Agent(Document):
    ID=IntField(primary_key=True)
    category=StringField()
    name=StringField()
    location=StringField()
    whatsapp=IntField()
    mobile_number=IntField()
    email=StringField()
    always=BooleanField()
    meta = {'indexes': [
        {'fields': ['$name', "$location"],
         'default_language': 'english',
         'weights': {'name': 5, 'location': 5}
        }
    ]}


def add_documents(dbname,update_dict):
    """
    dbname='userdb' or agentdb
    """
    connect(dbname)

    if dbname=='userdb':
        add=User(**update_dict)
    elif dbname=='agentdb':
        add=Agent(**update_dict)
    add.save()
    return 'document added'

def srch_documents(dbname,query):
    """
    dbname='userdb' or agentdb
    """    
    print(dbname)
    connect(dbname)

    if dbname=='userdb':

       res=json.loads(User.objects.search_text(query).to_json())
            #res_list.append(res)
        # res['id']=UserDB.__dict__['id']
        # res['name']=UserDB.__dict__['name']
        # res['mobile_number']=UserDB.__dict__['mobile_number']
        # res['email']=UserDB.__dict__['email']
        # res['date']=UserDB.__dict__['date']
        # res['comments']=UserDB.__dict__['comments']
        #add=UserDB(**update_dict)
    elif dbname=='agentdb':
        res=json.loads(Agent.objects.search_text(query).to_json())
    return res

def return_dataframe(dbname):
    connect(dbname)
    if dbname=='userdb':
        df=pd.DataFrame(json.loads(User.objects().to_json()),columns=user_schema)
        df['date']=df['date'].apply(lambda x:datetime.fromtimestamp(x['$date']/1000))
    elif dbname=='agentdb':
        df=pd.DataFrame(json.loads(Agent.objects().to_json()),columns=agent_schema)
    return df
def export_csv(dbname,csvfilename):
    print('Exporting {} to {}.csv'.format(dbname,csvfilename))
    df=return_dataframe(dbname)
    return df.to_csv(csvfilename,index=False)
def give_unique(dbname,feild):
    connect(dbname)

    if dbname=='userdb':
        temp=User.objects()
    elif dbname=='agentdb':
        temp=Agent.objects()
    return temp.distinct(feild)
def get_always():
    agent_schema=['id','category','name','location','whatsapp','mobile_number','email','always']
    connect('agentdb')
    temp=Agent.objects(always=True)
    return pd.DataFrame(json.loads(temp.to_json()),columns=agent_schema)

if __name__=='__main__':
    user_dict=dict(name='lasttry',mobile_number=9444532122,email='guru@gmail.com',
    date=datetime.strptime('29/09/2018','%d/%m/%Y'),comments='very good')
    agent_dict=dict(category='travel',name='lasttry ,agent',location='san francisco',whatsapp=94444526172,
    mobile_number = 874308230823,email='qba@gmail.com',always=True)


    add_documents('userdb',user_dict)
    add_documents('agentdb',agent_dict)
    query=input('Enter the query')
    print(srch_documents('agentdb',query))
    query=input('Enter the query')
    print(srch_documents('userdb',query))
    export_csv('userdb','userdb.csv')
    export_csv('agentdb','agentdb.csv')

# df=pd.DataFrame(json.loads(User.objects().to_json()),columns=user_schema)
# df['date'].apply(lambda x:datetime.fromtimestamp(x['$date']/1000))
# sam=df['date'][0]['$date']
# datetime.fromtimestamp(sam)

# datetime.utcfromtimestamp(sam).strftime('%Y-%m-%d %H:%M:%S')
# user_dict=dict(name='guru',mobile_number=9444532122,email='guru@gmail.com',
# date=datetime.strptime('29/09/2018','%d/%m/%Y'),comments='very good')
# s=User(**user_dict)
# s.save()

# arun=User.objects(name='guru')[0]
# pd.DataFrame(dict(json.loads(arun.to_json())))
# dir(arun)

# agent_dict=dict(category='travel',name='GURU',location='california',whatsapp=94444526172,
# mobile_number = 874308230823,email='qba@gmail.com',always=True)
# aa=Agent(**agent_dict)
# aa.save()

# search_res=Agent.objects.search_text('mass')
# search_res._mongo_query
# dir(search_res)

# inter=Agent.objects(location='california')
# inter.to_json()
# inter.filter(name='arun').to_json()
# inter.search_text('mass')
# dir(inter)

# inter=Agent.objects(name__iexact='guru')
# inter.to_json()
# s=User.objects()
# s.distinct('name')
# dir(s)