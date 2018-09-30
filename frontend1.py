# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 20:56:46 2018

@author: welcome
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt
from dash.dependencies import Input, Output
import plotly
import pandas as pd 
from whoosh.fields import *
import configparser
from search_eng import searchEngine
config = configparser.ConfigParser()
global_n_clicks=0
str_to_fn={
    'TEXT':TEXT(stored=True),
    'ID':ID(stored=True),
    'KEYWORD':KEYWORD(),
    'NUMERIC':NUMERIC,
    'DATETIME':DATETIME,
    'NGRAM':NGRAM


}
config.read('config.ini')
db_name=config['DB_NAME']['name']
schema=config['SCHEMA']
sch_dict=dict(schema.items())
#print([str_to_fn[v] for k,v in schema.items()])
sch_dict={k:str_to_fn[v] for k,v in sch_dict.items()}
se=searchEngine(db_name,sch_dict)
df=pd.DataFrame({'agent_name': 'vel', 'email': 'Enter email', 'loc': 'Enter loc', 'ph': 'Enter ph'},index=[1])

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
    return  html.Div([html.H5('Admin',style={'margin-left': '28%'}),html.Div(div),html.Button('Update',id='db-update'),
                                html.Div(id='db-update-output')],style={'margin-left': '457px'})

app=dash.Dash()
app.config['suppress_callback_exceptions']=True
#div=admin(sch_dict)
tab=dt.DataTable(                   rows=df.to_dict('records'),
                                            row_selectable=True,
                                            id='datatable',
                                            columns=df.columns,
                                            selected_row_indices=[])
app.layout=html.Div([
                     
                     html.H1('Search engine'),
                     dcc.Tabs(id='page-value',tabs=[
                                        {'label':'Admin','value':1},
                                        {'label':'Customer','value':2},],                                      
                                    vertical=True,
                                    style={'backgroundColor':'#2196F3','width':'20%'}),
                    html.Div(id='page-output'),  
                    #html.Div(tab,style={'width':'50%','margin-left': '457px'}),
                     ])

srchlayout=html.Div([html.Div([dcc.Input(id='search-input', 
                                           value='Search', type='text',
                                           style={'width': '49%','align':'center'}),
                                           html.Button('Search',id='search-button')],style={'align':'center','margin-left': '457px'}),
                                           #html.Div(id='datatable'),
                                           html.Div(tab,style={'width':'50%','margin-left': '457px'}),
                                           
                                            ])

@app.callback(Output('page-output', 'children'), [Input('page-value', 'value')])

def give_layout_for_outer_tabs(value):
    if value==1:
        return admin(sch_dict)
    if value==2:
        df=pd.DataFrame({'agent_name': 'vel', 'email': 'Enter email', 'loc': 'Enter loc', 'ph': 'Enter ph'},index=[1])

        #tab=dt.DataTable(rows=df.to_dict('records'),
         #                            id='search-results',
         #                           row_selectable=True,
         #                         columns=list(sch_dict.keys()),
         #                            selected_row_indices=[])
        
        return srchlayout
        return html.Div([html.Div([dcc.Input(id='search-input', 
                                           value='Search', type='text',
                                           style={'width': '49%','align':'center'}),
                                           html.Button('Search',id='search-button')],style={'align':'center','margin-left': '457px'}),
                                           #html.Div(id='datatable'),
                                           html.Div(tab,style={'width':'50%','margin-left': '457px'}),
                                           
                                            ])
    return None
    

app.css.append_css({
    'external_url': ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                     'https://cdnjs.cloudflare.com/ajax/libs/vis/4.20.1/vis.min.css',]
})

update_input=[Input( k, 'value') for k in sch_dict.keys() ]
update_input.append(Input('db-update','n_clicks'))
@app.callback(Output('db-update-output', 'children'),update_input ) 
def update_db(*lot):
    global global_n_clicks
    n_clicks=list(lot)[-1] # which returns n_clicks 
    if n_clicks==None:global_n_clicks=0
    print('n_clicks',n_clicks,global_n_clicks)
    
    if n_clicks!=None:
        if n_clicks-global_n_clicks>0:
            #print(n_clicks)
            print(lot)
            up_v=dict.fromkeys(sch_dict.keys())
            for idx,key in enumerate(up_v):
                up_v[key]=lot[idx]
            print(up_v)
            global_n_clicks=n_clicks
            se.add_documents(up_v)
            return 'updated'

def generate_table(dataframe):
    return (
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(len(dataframe))]
    )
    

@app.callback(Output('datatable', 'rows'),[Input('search-input','value'),Input('search-button','n_clicks')] ) 
def search_db(text,n_clicks):
    global global_srch_clicks
    if n_clicks==None:global_srch_clicks=0
    print('n_clicks',n_clicks,global_srch_clicks)
    if n_clicks!=None:
        if n_clicks-global_srch_clicks>0:
            res=se.search_index('agent_name',text)
            print(res)
            df=pd.DataFrame(res,index=range(int(len(res)/4)))
            print(df.head())
            print(list(sch_dict.keys()))
            tab=dt.DataTable(rows=df.to_dict('records'),
                                            row_selectable=True,
                                            columns=list(sch_dict.keys()),
                                            selected_row_indices=[])
            
            #print(df.shape,df)
            #return generate_table(df)
            global_srch_clicks=n_clicks
            print(tab)
            #return html.Div(tab)
            return df.to_dict('records')
if __name__=='__main__':
    app.run_server(debug=True,host='0.0.0.0')

    