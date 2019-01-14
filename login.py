from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
driver = webdriver.Firefox()
driver.implicitly_wait(10)
driver.get("https://webadvisor.allegheny.edu/")
elem = driver.find_elements_by_id("acctLogin")
if len(elem) > 0:
    elem[0].click()
username = driver.find_element_by_name("USER.NAME")
password = driver.find_element_by_name("CURR.PWD")
enterKey = driver.find_element_by_name("SUBMIT2")
username.send_keys("millerc8")
password.send_keys("Euleristtoll2019!")
enterKey.click()
elem2 = driver.find_element_by_partial_link_text("Students")
elem2.click()
elem3 = driver.find_element_by_partial_link_text("Enter")
elem3.click()
year = Select(driver.find_element_by_name('FA.YEAR'))
year.select_by_index(1)
enterKey2 = driver.find_element_by_name("SUBMIT2")
enterKey2.click()