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
global_quote_clicks=0
global_srch_clicks=0
config.read('config.ini')
db_name=config['DB_NAME']['name']
schema=config['SCHEMA']
sch_dict=dict(schema.items())
#print([str_to_fn[v] for k,v in schema.items()])
sch_dict={k:str_to_fn[v] for k,v in sch_dict.items()}
se=searchEngine(db_name,sch_dict)
df=pd.DataFrame({'agent_name': 'example', 'email': 'Enter email', 'loc': 'Enter loc', 'ph': 'Enter ph'},index=[1])

app=dash.Dash()
app.config['suppress_callback_exceptions']=True
tab=dt.DataTable(                   rows=[{}],
                                            row_selectable=True,
                                            id='datatable',
                                            columns=df.columns,
                                            selected_row_indices=[])

info_layout=html.Div([
                    html.Div([html.H5('From :'),dcc.Input(id='from-add', 
                                           value='from', type='text',
                                           style={'width': '20%','align':'center'}),
                    html.Div([html.H5('To :'),dcc.Input(id='to-input', 
                                           value='Search', type='text',
                                           style={'width': '49%','align':'center'})])],className='row'),
                    html.Div([html.H5('Name :'),dcc.Input(id='name-add', 
                                           value='from', type='text',
                                           style={'width': '49%','align':'center'})]),
                    html.Div([html.H5('Mobile Number :'),dcc.Input(id='mob-add', 
                                           value='from', type='text',
                                           style={'width': '49%','align':'center'})]),
                    html.Div([html.H5('Email :'),dcc.Input(id='email-add', 
                                           value='from', type='text',
                                           style={'width': '49%','align':'center'})]),
                    html.Button('Send Details',id='senddetails')
                    ])
srchlayout=html.Div([html.Div([dcc.Input(id='search-input', 
                                           value='Search', type='text',
                                           style={'width': '49%','align':'center'}),
                                           html.Button('Search',id='search-button')],style={'align':'center','margin-left': '457px'}),
                                           #html.Div(id='datatable'),
                                           html.Div(tab,style={'width':'50%','margin-left': '457px'}),
                                           html.Button('Get Quote',id='getquote'),
                                           html.Div(id='quote-output'),
                                            ])

                                        
app.layout=srchlayout
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
@app.callback(Output('quote-output', 'children'),[Input('getquote','n_clicks')] ) 

def get_quote(n_clicks):
    global global_quote_clicks
    if n_clicks==None:global_quote_clicks=0
    print('n_clicks',n_clicks,global_quote_clicks)
    if n_clicks!=None:
        if n_clicks-global_quote_clicks>0:
            print('inside',n_clicks,global_quote_clicks)
            global_quote_clicks=n_clicks
            return info_layout  
app.css.append_css({
    'external_url': ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                     'https://cdnjs.cloudflare.com/ajax/libs/vis/4.20.1/vis.min.css',]
})
if __name__=='__main__':
    app.run_server(debug=True,host='192.168.55.96',port=8051)
