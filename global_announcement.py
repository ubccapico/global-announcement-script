# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 11:12:29 2018

@author: Adam Dixon and Jeremy Hidjaja
"""
from dateutil import parser
import re
try:
    import requests
except:
    import pip
    pip.main(['install', 'requests'])
    import requests
try:
    import pandas as pd
except:
    import pip
    pip.main(['install', 'pandas'])
    import pandas as pd

# Populate parameters as global variables
ss = pd.read_csv("announcement_parameters.csv")
df = pd.DataFrame(columns = ['url', 'start_date', 'end_date', 'start_time',
                             'end_time', 'subject', 'message', 'account_id'])
for index, row in ss.iterrows():
    url = row['url']
    start_date = row['start_date']
    end_date = row['end_date']
    start_time = row['start_time']
    end_time = row['end_time']
    subject = row['subject']
    message = row['message']
    account_id = row['account_id']
    
with open('Canvas API Token.txt') as f:
    token = f.read() 

def convert_pdt_utc(time_string):
    time_split = re.split(r"\:", time_string)
    time_hour_utc = int(time_split[0]) + 8


    if(time_hour_utc >= 24):
        time_hour_utc -= 24

    time_return = 'T{}:{}:00Z'.format(time_hour_utc, time_split[1])
    return time_return


def make_announcement():
    start_at = parser.parse(start_date + convert_pdt_utc(start_time))
    end_at = parser.parse(end_date + convert_pdt_utc(end_time))
    
    r = requests.post(url + "accounts/" + str(account_id) + "/account_notifications",
                      headers = {'Authorization': 'Bearer ' + str(token)},
                      params = {"account_notification[subject]" : subject,
                                "account_notification[message]" : message,
                                "account_notification[start_at]" : start_at,
                                "account_notification[end_at]" : end_at})
    return r

boolean = input("Would you like to post your global announcement? Type y for yes or n for no: ")
if boolean is 'y':
    r = make_announcement()
    if r.ok:
        print()
        print("Success! Your announcement will be posted at " + start_time + " on " + start_date + " until " + end_time + " on " + end_date + "\n")
        print("Your subject is: " + subject + "\n")
        print("Your message is: " + message)
        