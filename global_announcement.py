# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 11:12:29 2018

@author: Adam Dixon and Jeremy Hidjaja
"""
from dateutil import parser
from datetime import datetime
import getpass, requests, pandas as pd, pytz

def make_announcement(url, start_date, end_date, start_time, end_time, subject, message, account_id, token):
    
    local = pytz.timezone("America/Vancouver")
    s_date = start_date.split("/")
    s_time = start_time.split(":")
    start_at = datetime(int(s_date[2]), int(s_date[0]), int(s_date[1]), int(s_time[0]), int(s_time[1]), 0, 0, local)
    start_at = parser.parse(start_at.astimezone(pytz.UTC).isoformat()[:-6]+ 'Z')
        
    e_date = end_date.split("/")
    e_time = end_time.split(":")
    end_at = datetime(int(e_date[2]), int(e_date[0]), int(e_date[1]), int(e_time[0]), int(e_time[1]), 0, 0, local)
    end_at = parser.parse(end_at.astimezone(pytz.UTC).isoformat()[:-6] + 'Z')
    
    r = requests.post("{}/api/v1/accounts/{}/account_notifications".format(url, account_id), 
                      headers = {'Authorization': 'Bearer ' + str(token)},
                      params = {"account_notification[subject]" : str(subject),
                                "account_notification[message]" : str(message),
                                "account_notification[start_at]" : start_at,
                                "account_notification[end_at]" : end_at})
    return r

if __name__ == "__main__":
    # Populate parameters as global variables
    ss = pd.read_csv("announcement_parameters.csv")
    df = pd.DataFrame(columns = ['start_date (m/d/y)', 'end_date (m/d/y)', 'start_time (HH:MM (24 hour))',
                                 'end_time (HH:MM (24 hour))', 'subject', 'message', 'account_id'])
    
    boolean = input("Would you like to post your global announcements? Type y for yes or n for no: ")
    if boolean is 'y':
        token = getpass.getpass("Enter your token: ")
        url = 'https://canvas.ubc.ca/'
        for index, row in ss.iterrows():
            start_date = row['start_date (m/d/y)']
            end_date = row['end_date (m/d/y)']
            start_time = row['start_time (HH:MM (24 hour))']
            end_time = row['end_time (HH:MM (24 hour))']
            subject = row['subject']
            message = row['message']
            account_id = row['account_id']
            
            r = make_announcement(url, start_date, end_date, start_time, end_time, subject, message, account_id, token)
            
            if r.ok:
                print()
                print("Success! Your announcement will be posted at " + start_time + " on " + start_date + " until " + end_time + " on " + end_date + "\n")
                print("Your subject is: " + subject + "\n")
                print("Your message is: " + message)
            else:
                print()
                print("Failed to post announcement {}. {}".format(subject, r))
        