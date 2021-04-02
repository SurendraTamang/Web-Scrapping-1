import smtplib
from email.message import EmailMessage
import pandas as pd
import os
import time
import random


def send_email(username, passwd, fromUser, sub, body, to):
    msg = EmailMessage()
    msg['Subject'] = sub
    msg['From'] = fromUser
    msg['To'] = to
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(username, passwd)    
        smtp.send_message(msg)


if __name__ == "__main__":
    #-- Reading the input file --#
    df = pd.read_excel('inputFile.xlsx')

    #-- Setting configuration for mail --#
    EMAIL_USER = os.environ.get('EMAIL_USER')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')
    FROM = 'MyCompany'
    SUBJECT = "Test Subject"
    SIGNATURE = "Thanks\nABC XYZ"    

    for _,val in df.iterrows():
        if not isinstance(val['Business'], float):
            body = f'''Hi {val['First Name']},\n\nNice to see you are a Entrepreneur and owner of the business {val['Business']}\n\n{SIGNATURE}'''
        else:
            body = f'''Hi {val['First Name']},\n\nNice to see you are a Entrepreneur.\n\n{SIGNATURE}'''
        print(f'''Sending mail to <{val['Email']}> ....''')
        send_email(EMAIL_USER, EMAIL_PASS, FROM, SUBJECT, body, val['Email'])

        time.sleep(random.randint(3,6))



