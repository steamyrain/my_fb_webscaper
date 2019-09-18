import pymongo
import requests
import yaml
import datetime
import time
import random
from selenium.webdriver import (Chrome,Firefox,ChromeOptions,FirefoxProfile)
from selenium.webdriver.common.keys import Keys

class FbWebScraper():

    def __init__(self,my_email,my_password,my_profile_url,statuses=50,scroll_time=7,webdriver='Chrome'):
        
        # set account manually (temporary) 
        self.my_email = my_email
        self.my_password = my_password
        self.my_profile_url = my_profile_url
        self.number_of_statuses = statuses 
        self.scroll_time = scroll_time

        # initialize connection 
        self.mongo_connection = pymongo.MongoClient()
        self.db = self.mongo_connection['test']
        self.fb_statuses = self.db['fb-statuses']
        
        # set browser for scraping
        self.set_webdriver(webdriver)
    
        # check friends dict
        person_dict = self.fb_statuses.find_one({'friends_dict':{'$exists':True}})
        if person_dict == None:
            self.friends_dict = {}
        else:
            self.friends_dict = person_dict['friends_dict']

    def set_webdriver(self,webdriver):
        
        # Chrome
        if webdriver == 'Chrome':
            options = ChromeOptions()
            options.add_argument('--disable-notification')
            self.webdriver = Chrome('chromedriver/chromedriver',options=options)
        elif browser == 'Firefox':
            profile = FirefoxProfile()
            profile.set_preference('dom.webnotifications.enabled',False)
            self.webdriver = Firefox(firefox_profile=profile)

    def fb_login(self):
        self.webdriver.get('https://m.facebook.com')
        email = self.webdriver.find_element_by_id('m_login_email')
        password = self.webdriver.find_element_by_name('pass')
        email.send_keys(self.my_email)
        password.send_keys(self.my_password)
        password.send_keys(Keys.RETURN)
        #self.webdriver.close()

if __name__ == '__main__':
    with open('fb_login_credential.yaml','r') as stream:
        try:
            creds = yaml.load(stream)
            my_password = creds['password']
            my_email = creds['email']
            my_profile_url = creds['profile_url']
        except yaml.YAMLError as exc:
            print(exc)
            
    params = {'my_password':my_password,
            'my_email':my_email,
            'my_profile_url':my_profile_url,
            'webdriver':'Chrome'
            }
    fbScraper = FbWebScraper(**params)
    fbScraper.fb_login()
