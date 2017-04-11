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

# read config json from path
def get_config(config):
    with open(config, 'r') as f:
        return json.loads(f.read())

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
    
    # get config from path
    config = get_config(args.config)

    #get all items to parse
    items = config['item-to-parse']

    while True and len(items):
        nowtime = datetime.now()
        nowtime_Str = nowtime.strftime('%Y-%m-%d %H:%M:%S')
        print ('[%s] Start Checking' % (nowtime_Str))

        itemIndex = 1
        for item in copy(items):
            # url to parse
            item_page_url = urlparse.urljoin(config['base_url'], item[0])
            print('[#%02d] Checking price for %s (target price: %s)' % ( itemIndex, item[0], item[1]))

            itemIndex += 1

        if len(items):
            # time interval add some random number for preventing banning
            nowtime = datetime.now()
            thisIntervalTime = intervalTimeBetweenCheck + random.randint(0,150)

            #calculate next triggered time
            dt = datetime.now() + timedelta(seconds=thisIntervalTime)
            print('Sleeping for %d seconds, next start at %s' % (thisIntervalTime, dt.strftime('%Y-%m-%d %H:%M:%S')))
            time.sleep(thisIntervalTime)
        else:
            break


if __name__ == '__main__':
    main()