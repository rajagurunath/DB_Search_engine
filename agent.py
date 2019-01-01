import urllib
import numpy as np
import dash_auth
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt
from dash.dependencies import Input, Output
import plotly
import pandas as pd 
from mongodb_tables import add_documents,return_dataframe
from utility import dataframe
import configparser

#from search_eng_layout import srchlayout
config = configparser.ConfigParser()
update_clicks=0
export_n_clicks=0

config.read('config.ini')
db_name=config['DB_NAME']['name']
schema=config['SCHEMA']

VALID_USERNAME_PASSWORD_PAIRS = [
    [config['login_details']['usr'],config['login_details']['pw']]
]

df=pd.DataFrame({'agent_name': 'vel', 'email': 'Enter email', 'loc': 'Enter loc', 'ph': 'Enter ph'},index=[1])
agent_schema=['id','category','name','location','whatsapp','mobile_number','email','always']
agent_schema=[i.title() for i in agent_schema]
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

df=return_dataframe('agentdb')
df.columns=df.columns.str.title()
app=dash.Dash()
app.config['suppress_callback_exceptions']=True

auth = dash_auth.BasicAuth(
     app,
     VALID_USERNAME_PASSWORD_PAIRS
)
server = app.server
#df1=pd.DataFrame(np.nan,columns=agent_schema)
#df=df.append(df1,ignore_index=False)

print(df.to_dict('records'))
d=dict.fromkeys(agent_schema)
tab=dt.DataTable(
                rows=df.to_dict('records'),
                editable=True,
                id='datatable',
                row_selectable=True,
                row_update=True,
                columns=agent_schema,
                )


adminlayout=html.Div([
                     
                    html.H3('Admin page'),
                    html.Div([
                    html.A(html.Button('Update Record'),id='update-record',href='/details',
                                                                style={'margin-left': '100px'}),
                    html.A(html.Button('Export Record'),id='export-record',href='/export',
                                                                style={'margin-left': '100px'}),
                           ],className='row'),
                                 
                    ])
                    
agentDetails=html.Div([
                    html.H3('Admin Details'),
#                    html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}),
                    html.Div(tab,style={'width':'80%','margin-left': '100px'}),

                    #html.Div(tab,style={'width':'60%','margin-left': '400px'}),
                    html.Br(),
                    
                    html.Div(html.Button('Update',id='update-button'),style={'width':'90%','margin-left': '400px'}),
                    html.Br(),
                    html.Div(id='db-update-output'),

                    ])

exportlayout=html.Div([
        html.A(html.Button('Home'),id='home',href='/',
                                        style={'margin-left': '10px'}),
        
       html.Div([html.Br(),html.Div(dcc.RadioItems(id='dbname',        options=[
                                            {'label': 'Agent Details', 'value': 'agentdb'},
                                            {'label': 'Customer Details', 'value': 'userdb'},
                                            ],
                                            value='agentdb',
                                            labelStyle={'display': 'inline-block'}),
                                            style={'margin-left': '1px','width':'55%'},
                                            ),
                    html.Br(),
                    html.Div(id='export-button')]
                                            ,style={'width':'90%','margin-left': '30%',
                                            'marin-top':'50%'}
                                           ,className='column' )])
                    #html.Div(id='export-output')
                
                    # html.Div([html.H5('Admin',style={'margin-left': '28%'}),,
                    #             html.Button('Update',id='db-update'),
                    #             html.Div(id='db-update-output')],style={'margin-left': '457px'}),
#                     ])

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
                    
app.title='ADMIN'
#app.layout=adminlayout
app.layout=html.Div([dcc.Location(id='url', refresh=False),
                    html.Div(id='main-layout'),
                        html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'})
])

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

@app.callback(dash.dependencies.Output('main-layout', 'children'),
              [dash.dependencies.Input('url', 'pathname')])

#@app.callback(Output('main-layout', 'children'),[Input('getquote','n_clicks')] ) 
def return_layout(pathname):
    #print('pathname',pathname)
    if pathname=='/':
        #print('ind')
        return adminlayout
    elif pathname=='/details':
        return agentDetails
        return html.Div(info_layout,style={'width':'100%','margin-left': '100px'})
    elif pathname=='/export' :
        return exportlayout
    

    
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
    df=return_dataframe(dbname)
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

def str2bool(v):
  return v.lower() in ("yes", "true","y")


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
            try:
                df=pd.DataFrame(rows)
                df.dropna(inplace=True)
                df['always']=df['always(Y/N)'].apply(str2bool)
                #df['always']=df['always'].apply(bool)
                df.drop('always(Y/N)',axis=1,inplace=True)
                #print(df.dtypes)
                df=df.dropna()
                df.columns=df.columns.str.replace('id','ID')
                for dict_ in df.to_dict('records'):
                    add_documents('agentdb',dict_)
    
                update_clicks=n_clicks
            except Exception as e:
                return html.H6('Update failed due to {}'.format(e))
            return html.H6('updated')
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


