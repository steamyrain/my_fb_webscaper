import pymongo
import requests
import yaml
import datetime
import time
import random
import re
from selenium.webdriver import (Chrome,Firefox,ChromeOptions,FirefoxProfile)
from selenium.webdriver.common.keys import Keys

class FbWebScraper():

    def __init__(self,my_email,my_password,my_profile_url,statuses=50,wait_time=5,scroll_time=7,webdriver='Chrome'):
        
        # set account manually (temporary) 
        self.my_email = my_email
        self.my_password = my_password
        self.my_profile_url = my_profile_url
        self.number_of_statuses = statuses 
        
        # set arbitrary scroll time for scraping 
        self.scroll_time = scroll_time

        # set arbitrary wait time for scraping 
        self.wait_time = wait_time

        # initialize connection with mongodb
        self.mongo_connection = pymongo.MongoClient()
        self.db = self.mongo_connection['test']
        self.fb_statuses = self.db['fb-statuses']
        
        # set webdriver for scraping
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
            options.add_argument('--disable-notifications')
            self.webdriver = Chrome('chromedriver/chromedriver',options=options)

        # Firefox
        elif browser == 'Firefox':
            profile = FirefoxProfile()
            profile.set_preference('dom.webnotifications.enabled',False)
            self.webdriver = Firefox(firefox_profile=profile)

    def fb_login(self):
        
        # initialize webdriver
        self.webdriver.get('https://www.facebook.com')
        
        # find email input box 
        email = self.webdriver.find_element_by_id('email')
        
        # find password input box
        password = self.webdriver.find_element_by_id('pass')
        
        # send keys to each element accordingly
        email.send_keys(self.my_email)
        password.send_keys(self.my_password)
        
        # press enter on password element (in m.facebook it will bring you to confirmation page)
        password.send_keys(Keys.RETURN) 
        
        # wait the page to load 
        time.sleep(self.wait_time)

        
    def set_friends_dict(self):
        m_facebook = 'https://m.facebook.com'
        facebook = 'https://www.facebook.com'
        if self.my_profile_url.startswith(m_facebook):
            profile_name = re.sub("^"+m_facebook,"",self.my_profile_url)
        elif self.my_profile_url.startswith(facebook):
            profile_name = re.sub("^"+facebook,"",self.my_profile_url)
        self.webdriver.find_element_by_css_selector(f'a[href*="{profile_name}"]').click()
        time.sleep(self.wait_time)
        self.webdriver.find_element_by_css_selector('a[data-tab-key="friends"]').click()
        time.sleep(self.wait_time)
        self.number_of_friends = int(self.webdriver.find_element_by_name('All friends').find_element_by_xpath('span[2]').text)
        
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
    fbScraper.set_friends_dict()
