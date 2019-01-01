from faker import Faker
import sqlite3
import pandas as pd
from string import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
credentials=config['Web_credentials']

def fake_data_generator(n_rows=100):
    fake = Faker()
    list_of_tuples=[]
    for _ in range(n_rows):
        list_of_tuples.append((fake.name(),fake.phone_number(),fake.address(),fake.email(),
                               ))
    return pd.DataFrame(list_of_tuples,columns=['name','PH','address','email'])


def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)
def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails
def dataframe(dbname):
        
    path='{}.db'.format(dbname)
    conn=sqlite3.connect(path)
    if dbname=='userdb':table='usertable'
    if dbname=='agentdb':table='agenttable'
    df=pd.read_sql('select * from {}'.format(table),conn)
    conn.close()
    return df
def export_csv(self,csvfilename):
    return self.dataframe(self.config['dname']).to_csv(csvfilename,index=False)
def get_table_names(dbname):
    con = sqlite3.connect('{}.db'.format(dbname))
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return cursor.fetchall()
def get_always():
    agent_schema=['id','category','name','location','whatsapp','mobile_number','email','always']
    con = sqlite3.connect('agentdb.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM agenttable WHERE always='1';")
    return pd.DataFrame(cursor.fetchall(),columns=agent_schema)


def send_msg(names:list,emails:list,places:dict):
    """
    names,emails
    """
    try:
        #names, emails = get_contacts() # read contacts
        message_template = read_template('msg_template.txt')

        # set up the SMTP server
        MY_ADDRESS=credentials['email']
        PASSWORD=credentials['password']
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        #s.ehlo()

        s.starttls()
        s.login(MY_ADDRESS, PASSWORD)

        # For each contact, send the email:
        for name, email in zip(names, emails):
            msg = MIMEMultipart()       # create a message

            # add in the actual person name to the message template
            message = message_template.substitute(PERSON_NAME=name.title(),cust_name=places['name'],
                                                    mobile_number=places['mobile_number'],
                                                    email=places['email'],date=places['date'],comments=places['comments'])
            # message = message_template.substitute(cust_name=places[0])
            # message = message_template.substitute(mobile_number=places[1])
            # message = message_template.substitute(email=places[2])
            # message = message_template.substitute(date=places[3])
            # message = message_template.substitute(comments=places[4])

            # Prints out the message body for our sake
            #print(message)

            # setup the parameters of the message
            msg['From']=MY_ADDRESS
            msg['To']=email
            msg['Subject']="Customer details"
            
            # add in the message body
            msg.attach(MIMEText(message, 'html'))
            
            # send the message via the server set up earlier.
            s.send_message(msg)
            del msg
    except Exception as e:
        print('Email sent failed {}'.format(e))




if __name__=='__main__':
     sample_df=fake_data_generator()   
     sample_df.to_csv('sample_data.csv',index=False)     
     send_msg(['guru'],['gurunathrajagopal@gmail.com'],['test1']*5)






