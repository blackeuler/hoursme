from datetime import date
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

class TimeLogger():
    def __init__(self):
        #Create a Headless Browser
        options = Options()
        options.add_argument("--headless")
        options.binary_location =  os.environ['GOOGLE_CHROME_SHIM']
        DRIVER_PATH = os.environ['DRIVER_PATH']

        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH,chrome_options=options)
        self.driver.implicitly_wait(1)
        self.driver.set_page_load_timeout(10)
        self.driver.get("https://webadvisor.allegheny.edu/")
        self.user = None
        self.passw = None
        self.page = None
    
    def webRun(self):
        self.login(self.user,self.passw)
        self.jobMenu()
        jobs = self.showJobs()
        return jobs
     

    def login(self, user, passw):
        '''Logins in User to WebAdvisor Account'''
        if(self.page):
            self.driver.close()
            self.__init__()
        self.clickId("acctLogin")
        username = self.driver.find_element_by_name("USER.NAME")
        password = self.driver.find_element_by_name("CURR.PWD")
        username.send_keys(str(user))
        password.send_keys(str(passw))
        self.pressEnter()
        try:
            self.driver.find_element_by_class_name("errorText")
            return False
        except NoSuchElementException:
            self.page = 'loginDone'
            return True
    def webLogin(self):

        if(self.login(self.user,self.passw)):
            self.jobMenu()
            return True
        return False        
    
    def jobMenu(self):
        '''Navigates driver to jobMenu '''
        self.clickPartial("Students")
        self.clickPartial("Enter")
        year = Select(self.driver.find_element_by_name('FA.YEAR'))
        year.select_by_index(1)
        self.pressEnter()
    
    def selectJob(self, jobIndex): 
        jobid = f"JS_LIST_VAR8_{jobIndex}"
        print(f"Selecting Job{jobid}")
        self.clickId(jobid)
        self.pressEnter()

    def showJobs(self):
        jobList = []
        elem3 = self.driver.find_element_by_xpath("/html/body/div/div[2]/div[4]/div[4]/form/div[1]/div/table/tbody/tr[2]/td/div/table/tbody")
        for row in elem3.find_elements_by_xpath(".//tr"):
            jobList.append([td.text for td in row.find_elements_by_tag_name("td")])
        filtList = [x for x in jobList if x!=[]]
        filteredList = [[item[5],item[6],item[7]] for item in filtList]
        return filteredList

    def selectMonth(self,month):
        months = [0,7,8,9,10,11,12,1,2,3,4,5,6]
        month = months[month]
        monthid = f"LIST_VAR1_{month}"
        print(f"Selecting{month}")
        try:
            self.clickId(monthid)
            self.pressEnter()
        except:
            return False    
    def goToDay(self, day):
        try:
            startDateid = self.driver.find_element_by_id('LIST_VAR1_1').text.split('/')
        except NoSuchElementException:
            print("Couldnt find List VAR1_!")
            return False
        startDate = date(int(startDateid[2]),int(startDateid[0]),int(startDateid[1]))
        numTabsC = day - startDate
        try:
            self.clickId("LIST_VAR2_1")
        except NoSuchElementException:
            return False
        days = numTabsC.days 
        actions = ActionChains(self.driver)
        for _ in range(days):
            actions.send_keys(Keys.TAB)
        actions.perform()
        actions.reset_actions()

        
    def enterHours(self,hours):
        faction = ActionChains(self.driver)
        faction.send_keys(hours).perform()
        self.pressEnter()

    def pressEnter(self):
        enterKey2 = self.driver.find_element_by_name("SUBMIT2")
        enterKey2.click()
    def clickPartial(self, text):
        elem2 = self.driver.find_element_by_partial_link_text(str(text))
        elem2.click()
    def clickId(self, id):
        elem2 = self.driver.find_element_by_id(str(id))
        elem2.click()
    def close(self):
        self.driver.close()
