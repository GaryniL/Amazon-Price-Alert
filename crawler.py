#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import json
import time
import requests
import smtplib
import argparse
import urlparse
import datetime,random
import UserAgent

from copy import copy
from lxml import html
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date, datetime, timedelta

ua = UserAgent.UserAgent()
intervalTimeBetweenCheck = 0
dateIndex = datetime.now()
emailinfo = {}

# msg_content format
# msg_content['Subject'] = 'Subject'
# msg_content['Content'] = 'This is a content'
def send_email(msg_content):
    global emailinfo

    try:
        # Try to login smtp server
        s = smtplib.SMTP("smtp.gmail.com:587")
        s.ehlo()
        s.starttls()
        s.login(emailinfo['sender'], emailinfo['sender-password'])
    except smtplib.SMTPAuthenticationError:
        # Log in failed
        print smtplib.SMTPAuthenticationError
        print('[Mail]\tFailed to login')
    else:
        # Log in successfully
        print('[Mail]\tLogged in! Composing message..')

        for receiver in emailinfo['receivers']:

            msg = MIMEMultipart('alternative')
            msg['Subject'] = msg_content['Subject']
            msg['From'] = emailinfo['sender']
            msg['To'] = receiver
            
            text = msg_content['Content']

            part = MIMEText(text, 'plain')
            msg.attach(part)
            s.sendmail(emailinfo['sender'], receiver, msg.as_string())
            print('[Mail]\tMessage has been sent to %s.' % (receiver))


def checkDayAndSendMail():
    todayDate = datetime.now()
    start = datetime(todayDate.year, todayDate.month, todayDate.day)
    end = start + timedelta(days=1)
    global dateIndex

    # if change date
    if dateIndex < end :
        dateIndex = end
        # send mail notifying server still working
        print "==>>>>>>",dateIndex

# read config json from path
def get_config(config):
    with open(config, 'r') as f:
        # handle '// ' to json string
        input_str = re.sub(r'// .*\n', '\n', f.read())
        return json.loads(input_str)

# add some arguments 
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        default='%s/config.json' % os.path.dirname(os.path.realpath(__file__)),
                        help='Add your config.json path')
    parser.add_argument('-t', '--poll-interval', type=int, default=780,
                        help='Time(second) between checking, default is 780 s.')

    return parser.parse_args()

def main():
    #set up arguments
    args = parse_args()
    intervalTimeBetweenCheck = args.poll_interval
    global dateIndex
    global emailinfo

    dateIndex = datetime.now()

    # get config from path
    config = get_config(args.config)
    emailinfo = config['email']

    #get all items to parse
    items = config['item-to-parse']

    while True and len(items):
        nowtime = datetime.now()
        nowtime_Str = nowtime.strftime('%Y-%m-%d %H:%M:%S')
        print ('[%s] Start Checking' % (nowtime_Str))

        # send mail notify system working everyday
        checkDayAndSendMail()

        itemIndex = 1
        for item in copy(items):
            # url to parse
            item_page_url = urlparse.urljoin(config['amazon-base_url'], item[0])
            print('[#%02d] Checking price for %s (target price: %s)' % ( itemIndex, item[0], item[1]))

            price = random.randint(33400,33600)
            productName = item[2]
            # Check price lower then you expected
            if not price:
                continue
            elif price <= item[1]:
                print('[#%02d] %s\'s price is %s!! Trying to send email.' % (itemIndex,productName,price))
                msg_content = {}
                msg_content['Subject'] = '[AmazonJP] %s Price Alert - %s' % (productName,price)
                msg_content['Content'] = '[%s]\nThe price is currently %s !!\nURL to salepage: %s' % (nowtime_Str, price, item_page_url)
                send_email(msg_content)
                items.remove(item)
            else:
                print('[#%02d] %s\'s price is %s. Ignoring...' % (itemIndex,productName,price))

            itemIndex += 1


        if len(items):
            # time interval add some random number for preventing banning
            nowtime = datetime.now()
            thisIntervalTime = intervalTimeBetweenCheck + random.randint(0,150)

            # msg_content = {}
            # msg_content['Subject'] = 'Subject'
            # msg_content['Content'] = 'This is a content'
            # send_email(msg_content)

            #calculate next triggered time
            dt = datetime.now() + timedelta(seconds=thisIntervalTime)
            print('Sleeping for %d seconds, next time start at %s\n' % (thisIntervalTime, dt.strftime('%Y-%m-%d %H:%M:%S')))
            time.sleep(20)
        else:
            break


if __name__ == '__main__':
    main()