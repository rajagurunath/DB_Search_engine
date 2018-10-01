import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt
from dash.dependencies import Input, Output
import plotly
import pandas as pd 
from whoosh.fields import *
from dbclass import *
from utility import get_always,send_msg
import configparser
from search_eng import searchEngine
config = configparser.ConfigParser()
global_n_clicks=0
global_info_clicks=0
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
agent_schema=['id','category','name','location','whatsapp','mobile_number','email','always']
app=dash.Dash()
app.config['suppress_callback_exceptions']=True
tab=dt.DataTable(                   rows=[{}],
                                            row_selectable=True,
                                            id='datatable',
                                            columns=agent_schema[:-1],
                                            selected_row_indices=[])

info_layout=html.Div([
                    html.Div([
                                         html.Div(dcc.Dropdown(id='info-category-type',        options=[
                                            {'label': 'Travel', 'value': 'Travel'},
                                            {'label': 'Hotels', 'value': 'Hotels'},
                                            ],
                                            value='Travel'),
                                            style={'align':'center','width':'290px','height':'30%'},
                                            className='one columns'),
                                           dcc.Input(id='requirement', 
                                           value='requirement', type='text',
                                           style={'width': '49%','align':'center'},className='five columns'),
                                           ],
                                           className='row'),
                    html.Div([html.H5('Name :',className='two columns'),dcc.Input(id='info-name', 
                                           value='name', type='text',
                                           style={'width': '20%','align':'center'},className='Three columns')],className='row'),
                    html.Div([html.Div([
                        html.H5('Communication',style={'width':'20%'}),
                        html.H5('preferences',style={'width':'20%'})],className='Two columns'),
                        dcc.RadioItems(id='info-comm-type',
                                        options=[
                                            {'label': 'WhatsAPP', 'value': 'whatsapp'},
                                            {'label': 'Email', 'value': 'email'},
                                        ],
                                        value='MTL',
                                        labelStyle={'display': 'inline-block'},
                                    style={'width':'20%'},className='Two columns'),],className='row'),
                    html.Div([html.H5('contact details:',className='two columns'),dcc.Input(id='contact-details', 
                                           value='mob', type='text',
                                           style={'width': '20%','align':'center'},className='Three columns')],className='row'),
                    
                    html.Button('Send Details',id='senddetails'),
                    html.Div(id='thank-msg'),
                    ])
srchlayout=html.Div([html.Br(),html.Br(),html.Div([
                                         html.Div(dcc.Dropdown(id='category-type',        options=[
                                            {'label': 'Travel', 'value': 'Travel'},
                                            {'label': 'Hotels', 'value': 'Hotels'},
                                            ],
                                            value='Travel'),
                                            style={'align':'center','margin-left': '1px','width':'290px'},
                                            className='one columns'),
                                           dcc.Input(id='search-input', 
                                           value='Search', type='text',
                                           style={'width': '49%','align':'center'},className='five columns'),
                                           ],
                                           style={'align':'center','margin-left': '400px'},className='row'),
                                           html.Button('Search',id='search-button',style={'align':'center','margin-left': '400px'}),
                                           html.Br(),
                                           html.Br(),
                                           #html.Div(id='datatable'),
                                           html.Div(tab,style={'width':'60%','margin-left': '400px'}),
                                           html.Br(),
                                           html.Button('Get Quote',id='getquote',style={'margin-left': '400px'}),
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
            res=srch_documents('agentdb',text)
            print(res)

            df=pd.DataFrame(res,index=range(int(len(res))))
            print(df.head())
            #print(list(sch_dict.keys()))
            # tab=dt.DataTable(rows=df.to_dict('records'),
            #                                 row_selectable=True,
            #                                 columns=list(sch_dict.keys()),
            #                                 selected_row_indices=[])
            
            # #print(df.shape,df)
            # #return generate_table(df)
            global_srch_clicks=n_clicks
            # print(tab)
            # #return html.Div(tab)
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
            return html.Div(info_layout,style={'width':'100%','margin-left': '400px'})
@app.callback(Output('thank-msg', 'children'),[Input('info-category-type','value'),
Input('requirement','value'),
Input('info-name','value'),
Input('info-comm-type','value'),
Input('contact-details','value'),
Input('senddetails','n_clicks')] ) 
def info_layout_update(cat_type,requirement,name,comm_type,contact,n_clicks):
    global global_info_clicks
    if n_clicks==None:global_info_clicks=0
    print('n_clicks',n_clicks,global_info_clicks)
    if n_clicks!=None:
        if n_clicks-global_info_clicks>0:
    
            print(cat_type,requirement,name,comm_type,contact,n_clicks)
            user_schema=['name','mobile_number','email','date','comments']
            update_dict=dict.fromkeys(user_schema)
            update_dict['name']=name
            update_dict['date']=datetime.now()
            update_dict['comments']=requirement
            
            if comm_type=='whatsapp':
                update_dict['mobile_number']=contact
                update_dict['email']=None
            if comm_type=='email':
                update_dict['mobile_number']=None
                update_dict['email']=contact
            global_info_clicks=n_clicks
            add_documents('userdb',update_dict)
            return html.H4('Thanks for contacting,will share the quote shortly')
def send_mail(info,selected_names=None,selected_emails=None):
    """
    TODO: add selected rows from datatable
    """
    df=get_always()
    names=df['name'].tolist()
    emails=df['email'].tolist()
    names.extend(selected_names)
    emails.extend(selected_emails)
    send_msg(names,emails,info)
    return None
app.css.append_css({
    'external_url': ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                     'https://cdnjs.cloudflare.com/ajax/libs/vis/4.20.1/vis.min.css',]
})
if __name__=='__main__':
    app.run_server(debug=True,host='0.0.0.0',port=8051)
