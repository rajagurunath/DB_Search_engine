from faker import Faker
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


def send_msg(names:list,emails:list,places:list):
    """
    names,emails


    """
    
    names, emails = get_contacts() # read contacts
    message_template = read_template('message.txt')

    # set up the SMTP server
    MY_ADDRESS=credentials['email']
    PASSWORD=credentials['password']
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=name.title())

        # Prints out the message body for our sake
        print(message)

        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=email
        msg['Subject']="This is TEST"
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
        
if __name__=='__main__':
     sample_df=fake_data_generator()   
     sample_df.to_csv('sample_data.csv',index=False)     