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

# setup some arguments
# 1. config file path : default in same folder as code
# 2. poll interval time : default is 780 sec
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        default='%s/config.json' % os.path.dirname(
                            os.path.realpath(__file__)),
                        help='Set your path of config.json')

    parser.add_argument('-t', '--poll-interval', type=int, default=780,
                        help='Time in seconds between price checking')
    return parser.parse_args()


# read config file and load setting..
def get_config(config):
    with open(config, 'r') as f:
        return json.loads(f.read())