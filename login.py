from datetime import date
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains

def pressEnter(driver):
    enterKey2 = driver.find_element_by_name("SUBMIT2")
    enterKey2.click()
def clickPartial(driver, text):
    elem2 = driver.find_element_by_partial_link_text(str(text))
    elem2.click()
def clickId(driver, id):
    elem2 = driver.find_element_by_id(str(id))
    elem2.click()
options = Options()
options.headless = True
user = os.environ['YUSER']
passW = os.environ['PASS']
driver = webdriver.Firefox(options=options)
driver.implicitly_wait(3)
driver.get("https://webadvisor.allegheny.edu/")
clickId(driver,"acctLogin")
username = driver.find_element_by_name("USER.NAME")
password = driver.find_element_by_name("CURR.PWD")
username.send_keys(str(user))
password.send_keys(str(passW))
pressEnter(driver)
clickPartial(driver,"Students")
clickPartial(driver,"Enter")
year = Select(driver.find_element_by_name('FA.YEAR'))
year.select_by_index(1)
pressEnter(driver)
jobList = []
elem3 = driver.find_element_by_xpath("/html/body/div/div[2]/div[4]/div[4]/form/div[1]/div/table/tbody/tr[2]/td/div/table/tbody")
for row in elem3.find_elements_by_xpath(".//tr"):
    jobList.append([td.text for td in row.find_elements_by_tag_name("td")])
filtList = [x for x in jobList if x!=[]]
filteredList = [[item[5],item[6],item[7]] for item in filtList]
print(str(filteredList))
choice = int(input('Please pick a job'))  
jobid = f"JS_LIST_VAR8_{choice}"
clickId(driver, jobid)
pressEnter(driver)
months = [0,7,8,9,10,11,12,1,2,3,4,5,6]
monthSelection = int(input("Please enter your month"))
choice = months[monthSelection]
monthid = f"LIST_VAR1_{choice}"
clickId(driver, monthid)
pressEnter(driver)
startDateid = driver.find_element_by_id('LIST_VAR1_1').text.split('/')
print(startDateid)
startDate = date(int(startDateid[2]),int(startDateid[0]),int(startDateid[1]))
numTabsC = date.today() - startDate
tabStart = driver.find_element_by_id("LIST_VAR2_1")
tabStart.click()
print(str(numTabsC.days))
days = numTabsC.days 
print(str(days))
actions = ActionChains(driver)
for _ in range(days):
    actions.send_keys(Keys.TAB)
actions.perform()
actions.reset_actions()
faction = ActionChains(driver)
hours = input("Enter the Amount of Hours for today")
faction.send_keys(hours).perform()
pressEnter(driver)
driver.close()
