import os
import pandas as pd
from google.cloud import storage
import gzip
import csv
from datetime import datetime
import smtplib
from email.message import EmailMessage


try:
    td = pd.read_csv('./today.csv')
    yd = pd.read_csv('./yesterday.csv')
except:
    EMAIL_USER = os.environ.get('EMAIL_USER')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')

    msg = EmailMessage()
    msg['Subject'] = 'GOOGLE BUCKET SCRIPT ERROR ALERT: mymh community'
    msg['From'] = EMAIL_USER
    msg['To'] = 'p.byom26@gmail.com, henrytz369@gmail.com'
    msg.set_content(f'''Hi,\ngBucket.py encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}.\nThe error is: "The mymh community CSV file doesn't contain correct data. Script terminated without pushing data into Google Bucket".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/iretApartments/gBucket.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM''')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)    
        smtp.send_message(msg)
    os._exit(1)

def get_both_rows(today, yesterday, which=None):
    """Find rows which are different between two DataFrames."""
    comparison_df = today.merge(yesterday, indicator=True, how='outer')
    if which is None:
        diff_df = comparison_df[comparison_df['_merge'] == 'both']
    else:
        diff_df = comparison_df[comparison_df['_merge'] == which]
    return diff_df

def get_left_rows(today, yesterday, which=None):
    """Find rows which are different between two DataFrames."""
    comparison_df = today.merge(yesterday, indicator=True, how='outer')
    if which is None:
        diff_df = comparison_df[comparison_df['_merge'] == 'left_only']
    else:
        diff_df = comparison_df[comparison_df['_merge'] == which]
    return diff_df

def generate_file_name():
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M")
    return f"data_{dt_string}.csv.gz"

def upload_to_bucket(fname):
    storage_client = storage.Client.from_service_account_json("../residential-reits-c3f28011accf.json")
    bucket = storage_client.get_bucket("mymh_community")
    blob = bucket.blob(fname)
    blob.upload_from_filename(fname)

def main():
    # Generating the gzip csv file name
    fname = generate_file_name()

    # Formatiing the dataframe & writing into a gunzipped csv file
    df1 = get_both_rows(td, yd)
    df2 = get_left_rows(td, yd)
    df2.loc[df2['_merge'] == 'left_only', 'Timestamp'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    final_df = df1.append(df2, ignore_index=True)
    final_df.drop('_merge', inplace=True, axis=1)    
    final_df.to_csv(fname, index=False, compression='gzip')

    # Uploading the file to Google Cloud Bucket
    upload_to_bucket(fname)

    # Deleting the unwanted files & generating yesterday.csv
    os.remove('./today.csv')
    os.remove('./yesterday.csv')
    os.remove(fname)
    final_df.to_csv('./yesterday.csv', index=False)


main()
