import pymongo
import requests
import yaml
import datetime
import time
import random
from selenium.webdriver import (Chrome,Firefox,ChromeOptions,FirefoxProfile)

class Fb_Web_Scraper():

    def __init__(self,my_email,my_password,my_profile_url,statuses=50,scroll_time=7,browser='Chrome'):
        
        # set account manually (temporary) 
        self.my_email = my_email
        self.my_password = my_password
        self.my_profile_url = my_profile_url
        self.number_of_statuses = statuses 
        self.scroll_time = scroll_time
        self.mongo_client = set_mongo_connection()

        # initialize connection 
        self.mongo_connection = pymongo.MongoConnection()
        self.db = self.mongo_connection['test']
        self.fb_statuses = self.db['fb-statuses']
        
        # set browser for scraping
        self.set_browser(browser)
    
        # check friends dict
        person_dict = self.db.find_one({'friends_dict':{'$exists':True}})
        if self.friends_dict == None:
            self.friends_dict = {}
        else:
            self.friends_dict = person_dict['friends_dict']

    def set_browser(self,browser):

if __name__ == '__main__':
    print("Hello world!")

