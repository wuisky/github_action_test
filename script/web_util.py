#!/usr/bin/env python3

import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

import argparse


class Webot:
    def __init__(self, url):
        userdata_dir = 'UserData'
        options = Options()
        options.add_argument('--user-data-dir=' + userdata_dir)
        #options.add_argument('--headless')
        ua = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0'
        options.add_argument('--user-agent=' + ua)
        #options.add_argument('--user-agent=hogehoge')
        options.add_argument('--no-proxy-server')
        self.driver = webdriver.Chrome(options=options)
        self.top_url = url
        self.driver.get(url)

    def try_cmd(self, cmd, arg=''):
        try:
            ret = cmd(arg)
            return True, ret
        except:
            return False, None

    def wait_page(self, current_url, timeout=15):
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_changes(current_url))
            return True
        except:
            print('timeout. stay in same page')
            return False

    def wait_ack(self, cmd, timeout):
        current_url = self.driver.current_url
        cmd()
        return self.wait_page(current_url, timeout)

    def back_to_top(self):
        self.driver.get(self.top_url)

    def move_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
