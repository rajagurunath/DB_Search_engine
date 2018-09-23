import os

from faker import Faker
from whoosh.fields import *
from whoosh.index import create_in
from whoosh.qparser import QueryParser
import pandas as pd
os.chdir(r'E:\search_engine')

#schema = Schema(Agent_name=TEXT(stored=True), Ph=ID(stored=True), desc=TEXT,
#                email=ID(),
#                date=DATETIME())

    
#ix = create_in(SEARCH_NAME, schema)
class searchEngine(object):
    """
    wrapper for whoosh search engine 
    """
    
    def __init__(self,name,schema_dict):
        self.__SEARCH_NAME__=name
        self.schema_dict=schema_dict
        schema=self.create_schema()
        
        if not os.path.exists(self.__SEARCH_NAME__):
            os.mkdir(self.__SEARCH_NAME__)
    
        self.index = create_in(self.__SEARCH_NAME__, schema)
    def create_schema(self):
        """
        dict :
            keys:Name to be stored in the schema (col name)
            values :Type of the Data
        
        """
        schema =Schema(** self.schema_dict)
        
        return schema
        
    def add_documents(self,list_of_tuples):
        writer = self.index.writer()
#        print(type(writer))
        for t in list_of_tuples:
#            print(t)
            writer.add_document(Agent_name=t[0],Ph=t[1],desc=t[2],email=t[3],date=t[4])
        writer.commit()
        return 'docuemnt added'
    
    def search_index(self,feild,query_string):
        """
        feild :specify the feilds in which the search as to be made
        Query string: specify the text string to search the index
        """
        res=[]
        with self.index.searcher() as searcher:
            query = QueryParser(feild, self.index.schema).parse(query_string)
            results = searcher.search(query,limit=5,terms=True)
            res=results.docs()
            print(results.docs())
#            res.append(results[0])
#            print(results)
        return list(res)
    

#fake.name()     

def fake_data_generator(n_rows=10):
    fake = Faker()
    list_of_tuples=[]
    for _ in range(n_rows):
        list_of_tuples.append((fake.name(),fake.phone_number(),fake.text(),fake.email(),
                               fake.date()))
    
    return list_of_tuples
    

if __name__=='__main__':
     lot=fake_data_generator()   
     sample_df=pd.DataFrame(lot)
     db_name='clean_try'
     sch_dict=dict(Agent_name=TEXT(stored=True), Ph=ID(stored=True), desc=TEXT,
                             email=ID(),
                             date=DATETIME())
     se=searchEngine(db_name,sch_dict)
     se.add_documents(lot)
     print(sample_df.iloc[4,2].split(' ')[0])
#     print(se.search_index('desc',sample_df.iloc[4,2]))
     num=se.search_index('desc',sample_df.iloc[4,2].split(' ')[0])
     print(num)
     print(sample_df.iloc[num,2])
