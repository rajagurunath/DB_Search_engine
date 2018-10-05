# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 20:56:46 2018

@author: welcome
"""
import urllib
import dash_auth
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt
from dash.dependencies import Input, Output
import plotly
import simplejson

import pandas as pd 
from whoosh.fields import *
from dbclass import add_documents
from utility import dataframe
import configparser
from search_eng import searchEngine
#from search_eng_layout import srchlayout
config = configparser.ConfigParser()
update_clicks=0
export_n_clicks=0
str_to_fn={
    'TEXT':TEXT(stored=True),
    'ID':ID(stored=True),
    'KEYWORD':KEYWORD(),
    'NUMERIC':NUMERIC,
    'DATETIME':DATETIME,
    'NGRAM':NGRAM


}
VALID_USERNAME_PASSWORD_PAIRS = [
    ['hello', 'world']
]
config.read('config.ini')
db_name=config['DB_NAME']['name']
schema=config['SCHEMA']
sch_dict=dict(schema.items())
#print([str_to_fn[v] for k,v in schema.items()])
sch_dict={k:str_to_fn[v] for k,v in sch_dict.items()}
se=searchEngine(db_name,sch_dict)
df=pd.DataFrame({'agent_name': 'vel', 'email': 'Enter email', 'loc': 'Enter loc', 'ph': 'Enter ph'},index=[1])
user_schema=['id','name','mobile_number','email','date','comments']
agent_schema=['id','category','name','location','whatsapp','mobile_number','email','always']

#df=pd.DataFrame(columns=list(sch_dict.keys()))


def admin(schema):
    """
    {'agent_name': 'TEXT', 'ph': 'ID', 'loc': 'TEXT', 'email': 'ID'}
    """
    #div_list=[]
    #for k,v in schema.items():
    #    div_list.append(html.Div([html.H5(k),dcc.Input(id='{}'.format(k),value='Enter {}'.format(k), type=k)],className='row'))
    div=[html.Div([html.H5(k.title().replace('_',' '),className='four columns',style={'left-margin':'40%'}),dcc.Input(id='{}'.format(k),value='Enter {}'.format(k), type=k,className='four columns',style={'left-margin':'40%'})],className='row') for k in schema.keys()]

    print(div)
    return  html.Div([html.H5('Admin',style={'margin-left': '28%'}),html.Div(tab,style={'width':'60%','margin-left': '400px'})
                                ,html.Button('Update',id='db-update'),
                                html.Div(id='db-update-output')],style={'margin-left': '457px'})

df=dataframe('agentdb')

app=dash.Dash()
app.config['suppress_callback_exceptions']=True
#div=admin(sch_dict)
# auth = dash_auth.BasicAuth(
#     app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )
d=dict.fromkeys(agent_schema)
tab=dt.DataTable(
                rows=[d for i in range(10)],
                editable=True,
                id='datatable',
                row_selectable=True,
                row_update=True,
                columns=agent_schema,
                )


adminlayout=html.Div([
                     
                    html.H1('Search engine'),
                    html.Div(tab,style={'width':'60%','margin-left': '400px'}),
                    html.Br(),
                    html.Div(html.Button('Update',id='update-button'),style={'width':'90%','margin-left': '400px'}),
                    html.Br(),

                    html.Div([html.Div(dcc.Dropdown(id='dbname',        options=[
                                            {'label': 'Agent', 'value': 'agentdb'},
                                            {'label': 'User', 'value': 'userdb'},
                                            ],
                                            value='agentdb'),
                                            style={'align':'center','margin-left': '1px','width':'290px'},
                                            className='one columns'),
                    
                    html.Div(id='export-button',className='row',)]
                                            ,style={'width':'90%','margin-left': '400px'},className='row'),
                    html.Div(id='db-update-output'),
                    #html.Div(id='export-output')
                
                    # html.Div([html.H5('Admin',style={'margin-left': '28%'}),,
                    #             html.Button('Update',id='db-update'),
                    #             html.Div(id='db-update-output')],style={'margin-left': '457px'}),
                     ])

# index_page = html.Div([
#     dcc.Link('Admin Page', href='/adminpage'),
#     html.Br(),
#     dcc.Link('Search Engine', href='/SE'),
#     html.Br(),           
# ])
#  app.layout = html.Div([
#  dcc.Location(id='url', refresh=False),
#  html.Div(id='page-content'),
# ])
app.layout=adminlayout
    
server = app.server # the Flask app

# @app.callback(Output('page-content', 'children'),
#               [Input('url', 'pathname')])
# def display_page(pathname):
#     print(pathname)
#     if pathname == '/adminpage':
#         print('admin',adminlayout)
#         return adminlayout
#     elif pathname == '/SE':

#         """
#         datatable not working when passed with divs
#         """
        
#         return html.Label(['Link to search engine', html.A('link', href='192.168.55.96:8051')])

#     else:
#         return index_page


app.css.append_css({
    'external_url': ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                     'https://cdnjs.cloudflare.com/ajax/libs/vis/4.20.1/vis.min.css',]
})

@app.callback(Output('export-button', 'children'),
              [Input('dbname','value'),
              ])
def update_download_link_defect(dbname):
    """
    Update the download link with new data after every purging of 
    Duplicate testcases
    """
    
    # global export_n_clicks
    # if n_clicks==None:export_n_clicks=0
        
    # if n_clicks!=None:
    #     if n_clicks-export_n_clicks==1:
    df=dataframe(dbname)
    df.reset_index(drop=True,inplace=True)

#          df_copy.drop(selected_row_indices,inplace=True)

#         dff = df_copy
    
    csv_string = df.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    
    #export_n_clicks=n_clicks



    return html.A(
                    html.Button('Export'),
                    id='Export',
                    download="{}.csv".format(dbname),
                    href=csv_string,
                    target="_blank",
                    className='download-link') 


@app.callback(Output('db-update-output', 'children'),
              [Input('datatable','rows'),
              Input('update-button','n_clicks')
              ])
def update_db(rows,n_clicks):
    global update_clicks
    if n_clicks==None:update_clicks=0
    print('n_clicks',n_clicks,update_clicks)
    if n_clicks!=None:
        if n_clicks-update_clicks>0:
            df=pd.DataFrame(rows)
            df=df.dropna()
            for dict_ in df.to_dict('records'):
                add_documents('agentdb',dict_)
            
            update_clicks=n_clicks
            
            return 'updated'
# @app.callback(Output('db-update-output', 'children'),[Input('update-button','n_clicks')]) 
# def update_db(*lot):
#     global global_n_clicks
#     n_clicks=list(lot)[-1] # which returns n_clicks 
#     if n_clicks==None:global_n_clicks=0
#     print('n_clicks',n_clicks,global_n_clicks)

#     if n_clicks!=None:
#         if n_clicks-global_n_clicks>0:
#             #print(n_clicks)
#             print(lot)
#             up_v=dict.fromkeys(sch_dict.keys())
#             for idx,key in enumerate(up_v):
#                 up_v[key]=lot[idx]
#             print(up_v)
#             global_n_clicks=n_clicks
#             se.add_documents(up_v)
#             return 'updated'

# update_input=[Input( k, 'value') for k in sch_dict.keys() ]
# update_input.append(Input('db-update','n_clicks'))
# #@app.callback(Output('db-update-output', 'children'),update_input ) 
# def update_db(*lot):
#     global global_n_clicks
#     n_clicks=list(lot)[-1] # which returns n_clicks 
#     if n_clicks==None:global_n_clicks=0
#     print('n_clicks',n_clicks,global_n_clicks)
    
#     if n_clicks!=None:
#         if n_clicks-global_n_clicks>0:
#             #print(n_clicks)
#             print(lot)
#             up_v=dict.fromkeys(sch_dict.keys())
#             for idx,key in enumerate(up_v):
#                 up_v[key]=lot[idx]
#             print(up_v)
#             global_n_clicks=n_clicks
#             se.add_documents(up_v)
#             return 'updated'

def generate_table(dataframe):
    return (
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(len(dataframe))]
    )
    
# @app.callback(Output('datatable', 'rows'),[Input('search-input','value'),Input('search-button','n_clicks')] ) 
# def search_db(text,n_clicks):
#     global global_srch_clicks
#     if n_clicks==None:global_srch_clicks=0
#     print('n_clicks',n_clicks,global_srch_clicks)
#     if n_clicks!=None:
#         if n_clicks-global_srch_clicks>0:
#             res=se.search_index('agent_name',text)
#             print(res)
#             df=pd.DataFrame(res,index=range(int(len(res)/4)))
#             print(df.head())
#             print(list(sch_dict.keys()))
#             tab=dt.DataTable(rows=df.to_dict('records'),
#                                             row_selectable=True,
#                                             columns=list(sch_dict.keys()),
#                                             selected_row_indices=[])
            
#             #print(df.shape,df)
#             #return generate_table(df)
#             global_srch_clicks=n_clicks
#             print(tab)
#             #return html.Div(tab)
#             return df.to_dict('records')
if __name__=='__main__':
    app.run_server(debug=True,host='0.0.0.0')


