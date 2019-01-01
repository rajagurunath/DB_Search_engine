import dash
import plotly.graph_objs as go
from flask import Flask
from flask_recaptcha import ReCaptcha
import flask
from flask import render_template
from threading import Thread
import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt
from dash.dependencies import Input, Output
import plotly
import pandas as pd 
#from dbclass import *
from mongodb_tables import *
from utility import send_msg
import configparser
#from search_eng import searchEngine
config = configparser.ConfigParser()
global_n_clicks=0
global_info_clicks=0
verify=False
global_quote_clicks=0
global_srch_clicks=0
config.read('config.ini')
#db_name=config['DB_NAME']['name']
schema=config['SCHEMA']
host=config['SERVER']['host']
port=int(config['SERVER']['port'])
captcha_url=config['Recaptcha']['captcha_url']
secret_key=config['Recaptcha']['secret_key']
site_key=config['Recaptcha']['site_key']


server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)

agent_schema=['id','category','name','location','whatsapp','mobile_number','email','always']

recaptcha = ReCaptcha(app=server,secret_key=secret_key,site_key=site_key)

app.config['suppress_callback_exceptions']=True
tab=dt.DataTable(                   rows=[{}],
                                            row_selectable=True,
                                            id='datatable',
                                            columns=agent_schema[:-1],
                                            selected_row_indices=[])

#info layout



thanks_layout=html.Div([html.Img(src=r'https://pre00.deviantart.net/55d2/th/pre/i/2014/224/4/8/genie_by_vgafanatic-d2mf64y.jpg',
                                            className='three columns'),
                html.H4('Thanks for contacting,will share the quote shortly'),
                html.Br(),
                    html.A( html.Button('Close',id='close'),
                                                            href='/',style={'align':'center','margin-left': '20%'})],className='column')
def update_info_layout(list_of_dict):
    info_layout=html.Div([html.Img(src=r'https://ubisafe.org/images/aladdin-drawing-pencil-3.gif',
                        className='two columns'),
                    html.Div([
                    html.Div([                                        
                        html.Br(),
                        html.Div([html.Div(dcc.Dropdown(id='info-category-type',        
                                    options=list_of_dict,
                                            value='Travel'),
                                            style={'align':'center','width':'180px','height':'30%'},
                                            className='one columns'),
                          html.Div(dcc.Input(id='requirement', 
                          value='Enter your Requirements', 
                          type='text',
                                       style={'width': '87%','height':'36px','align':'center','margin-left':'1%'}),className='six columns')],
                                             className='row'),
                        html.Br(),
                    html.Div([html.H5('Name :',className='two columns'),dcc.Input(id='info-name', 
                                           value='name', type='text',
                                                              style={'width': '27%','align':'center','margin-left':'11%'},className='six columns')],
                                           className='row'),
                    html.Div([html.Div([
                        html.H6('Communication',style={'width':'10%'}),
                        html.H6('preferences',style={'width':'10%'})],className='two columns'),
                        dcc.RadioItems(id='info-comm-type',
                                        options=[
                                            {'label': 'WhatsAPP', 'value': 'whatsapp'},
                                            {'label': 'Email', 'value': 'email'},
                                        ],
                                        value='email',
                                        labelStyle={'display': 'inline-block'},
                                    style={'width':'30%','margin-top':'40px','margin-left':'11%'},
                                    className='six columns'),],
                                       className='row'),
                            html.Div(
                             dcc.Input(id='contact-details', 
                                           value='mob', type='text',
                                           style={'width': '27%','align':'center','margin-left':'24%'},className='six columns')

                            ,className='row'),
                             html.Br(),
                    html.Div(id='recaptcha',
                    children=html.Iframe(src=captcha_url,
                    style={'border': 'thin lightgrey solid','height':'25%','width':'50%'})),
                    html.A( html.Button('Send Details',id='senddetails'),
                                                            href='/thanks',
                                                                ),
                    html.Div(id='thank-msg'),
                    ])],className='eight columns')],className='row')
    return info_layout

def update_srch_layout(list_of_dict):
    srchlayout=html.Div([html.Img(src=r'https://upload.wikimedia.org/wikipedia/ar/archive/1/13/20180719221455%21Genie_%28Disney%29.gif',
                        style={'width':'20%'},className='two columns'),
                     html.Div([html.Br(),html.Br(),html.Div([
                                         html.Div(dcc.Dropdown(id='category-type',
                                            options=list_of_dict,
                                            value='Travel'),
                                            style={'align':'center','margin-left': '1px','width':'190px'},
                                            className='one columns'),
                                           dcc.Input(id='search-input', 
                                           value='Search', type='text',
                                           style={'width': '40%','align':'center'},className='five columns'),
                                           ],
                                           style={'align':'center','margin-left': '100px'},className='row'),
                                           html.Div([html.Br(),html.Br(),html.Button('Search',id='search-button',
                                           style={'align':'center','margin-left': '100px'}),],className='row'),
                                           #html.Br(),
                                           #html.Br(),
                                           html.Div(id='datatable'),
                                           html.Div(dcc.Graph(id='pl-table',),style={'display': 'none'})
                                           #html.Br(),
                                        #    html.A(html.Button('Get Quote'),id='getquote',href='/info',
                                        #                         style={'margin-left': '100px'})
                                            ],style={'width':'70%'},className='eight columns')],className='row')
    return srchlayout
app.title="USER"
app.layout=html.Div([dcc.Location(id='url', refresh=False),
                    html.Div(id='main-layout')])
@app.callback(Output('datatable', 'children'),[Input('search-input','value'),Input('search-button','n_clicks')] ) 
def search_db(text,n_clicks):
    global global_srch_clicks
    if n_clicks==None:global_srch_clicks=0
    if n_clicks!=None:
        if n_clicks-global_srch_clicks>0:
            res=srch_documents('agentdb',text)
            df=pd.DataFrame(res,index=range(int(len(res))))
            global_srch_clicks=n_clicks
            if df.empty:
                return html.Div(html.H2('Specified Service not available at the moment'))
            df['id']=list(range(len(df)))
            df=df[['name','location','email']]
            #return generate_table(df)
            return html.Div([html.Div(generate_table(df)), 
            html.A(html.Button('Get Quote'),id='getquote',href='/info',
                                                                style={'margin-left': '100px'})])



@app.callback(dash.dependencies.Output('main-layout', 'children'),
              [dash.dependencies.Input('url', 'pathname')])

def return_layout(pathname):
    if pathname=='/':
        uniq=give_unique('agentdb','category')
        list_of_dict=[{'label':ele.title(),'value':ele.title()} for ele in uniq]
        return update_srch_layout(list_of_dict)
    elif pathname=='/info' :
        uniq=give_unique('agentdb','category')
        list_of_dict=[{'label':ele.title(),'value':ele.title()} for ele in uniq]
        return update_info_layout(list_of_dict)
    elif pathname=='/thanks' :
        return thanks_layout

@server.route('/recaptcha')
def flask_captcha_temp():
    return render_template('flask_Recap_try.html',recaptcha=recaptcha.get_code())

@app.callback(Output('quote-output', 'children'),[Input('getquote','n_clicks')] ) 

def get_quote(n_clicks):
    global global_quote_clicks
    if n_clicks==None:global_quote_clicks=0
    if n_clicks!=None:
        if n_clicks-global_quote_clicks>0:
            global_quote_clicks=n_clicks
            uniq=give_unique('agentdb','category')
            list_of_dict=[{'label':ele.title(),'value':ele.title()} for ele in uniq]
            return html.Div(update_info_layout(list_of_dict),style=
            {'width':'100%','margin-left': '400px'})
@server.route("/verify-captcha", methods=["POST"])
def submit():
    global verify
    if recaptcha.verify():
        # SUCCESS
        
        verify=True
     #   print('sucess')
        return """<html>
                <body>

                <img src="https://otc.watch/wp-content/uploads/2018/02/Verified-400.png" 
                alt="Trulli" width="50" height="50">

                </body>
                </html>
                """
    else:
        verify=False
        # FAILED
        return """<html>
                <body>

                <img src="http://certificates-bootcamp.mit.edu/static/img/not-verified.png" 
                alt="Trulli" width="5" height="5">

                </body>
                </html>"""

@app.callback(Output('thank-msg', 'children'),
[Input('info-category-type','value'),
Input('requirement','value'),
Input('info-name','value'),
Input('info-comm-type','value'),
Input('contact-details','value'),
Input('senddetails','n_clicks'),
] ) 
def info_layout_update(cat_type,requirement,name,comm_type,contact,n_clicks):
    global verify
    global global_info_clicks
    if n_clicks==None:global_info_clicks=0
    if n_clicks!=None:
        if n_clicks-global_info_clicks>0:
            if verify:
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
                thr=Thread(target=send_mail,args=[update_dict])
                thr.start()
                verify=False
                return 


def generate_table(df):
    trace = go.Table(
    header=dict(values=list(df.columns.str.title()),
                fill = dict(color='#C2D4FF'),
                 align = ['left'] * 5),
    cells=dict(values=[df[col] for col in df.columns],
                fill = dict(color='#F5F8FF'),
                align = ['left'] * 5),)

    data = [trace] 
    fig=go.Figure(data=data)
    return dcc.Graph(id='pl-table',figure=fig,style={'height':'250px'})

def send_mail(info,selected_names=[],selected_emails=[]):
    """
    TODO: add selected rows from datatable
    """
    df=get_always()
    names=df['name'].tolist()
    emails=df['email'].tolist()
    if len(names)==0 and len(emails)==0:
        names=[]
        emails=[]
    
    names.extend(selected_names)
    emails.extend(selected_emails)
    send_msg(names,emails,info)
    return None
app.css.append_css({
    'external_url': ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                     'https://cdnjs.cloudflare.com/ajax/libs/vis/4.20.1/vis.min.css',]
})
app.scripts.append_script({'external_url':'https://www.google.com/recaptcha/api.js'})
if __name__=='__main__':
    app.run_server(debug=True,host=host,port=port)

