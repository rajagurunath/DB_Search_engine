import os

from faker import Faker
from whoosh.fields import *
from whoosh.index import create_in,open_dir
from whoosh.qparser import QueryParser
import pandas as pd
from utility import fake_data_generator
#os.chdir(r'D:\DB_Search_engine')
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

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
        else:
            self.index=open_dir(self.__SEARCH_NAME__)
    def create_schema(self):
        """
        dict :
            keys:Name to be stored in the schema (col name)
            values :Type of the Data
        
        """
        schema =Schema(** self.schema_dict)
        
        return schema
        
    def add_documents(self,dict_):
        writer = self.index.writer()
#        print(type(writer))
        #for k,v in dict_.items():
#            print(t)
            
            #writer.add_document()
        writer.add_document(**dict_)
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
            res=dict(results[0])
            print(results.docs())
#            res.append(results[0])
#            print(results)
        print(res)
        return res
    def get_all_documents(self):
        return self.index.searcher().documents()
class sqlitedb():
    def __init__():
        pass
    def searrch(self, parameter_list):
        pass
        
if __name__=='__main__':
     db_name=config['DB_NAME']['name']
     schema=config['SCHEMA']
     sch_dict=dict(schema.items())
     se=searchEngine(db_name,sch_dict)
     se.add_documents(lot)
     print(sample_df.iloc[4,2].split(' ')[0])
#     print(se.search_index('desc',sample_df.iloc[4,2]))
     num=se.search_index('desc',sample_df.iloc[4,2].split(' ')[0])
     print(num)
     print(sample_df.iloc[num,2])
    # from whoosh.query import *
    # from whoosh.qparser import MultifieldParser
    # ix=open_dir(r'F:\searchEngine\DB_Search_engine\Database\UserDB')
    # query_string='guru'
    # list(ix.searcher().documents())
    # with ix.searcher() as searcher:
    #     parser = MultifieldParser(['name','location'], ix.schema)
    #     parser.parse(query_string)
    #     results = searcher.search(query,limit=5,terms=True)
    #     for hit in results:
    #         print(hit['name'])
    #     print(results[0])    
