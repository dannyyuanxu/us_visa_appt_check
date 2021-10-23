# this script opens up page and check available dates location

#### set up
import pandas as pd
import yaml
import time
import random
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import os
import dotenv

# read in config
with open('config.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    config = yaml.load(file, Loader=yaml.FullLoader)

login_site = config["reschedule_web"]
avail_data_loc = config["avail_data_loc"]
user_profile_data_loc = config["user_profile_data_loc"]

# read in the desired 
user_list = pd.Series(os.listdir(user_profile_data_loc))
user_list = list(user_list[~user_list.str.startswith('.')])




#### webpage operations

# open a browser
driver = Chrome()

# open page and log in
driver.get(login_site)
ok_to_login=driver.find_elements_by_xpath("//button[contains(string(), 'OK')]")[0]
ok_to_login.click()


username_field = driver.find_element_by_name("user[email]")
username_field.clear()
username_field.send_keys(login_username)

password_field = driver.find_element_by_name("user[password]")
password_field.clear()
password_field.send_keys(login_password)

policy_check = driver.find_element_by_xpath("//input[@name='policy_confirmed']")
driver.execute_script("arguments[0].click();", policy_check)

sign_in_button = driver.find_element_by_name("commit")
sign_in_button.click()





# click the earliest available date
#TODO inspect the dates, save to offline doc and upload to online account
while True:
    try:
        wait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, "//td[@data-handler='selectDay']"))).click()

        break
    except:
        driver.find_element(By.XPATH,  "//div[@class='ui-datepicker-group ui-datepicker-group-last']//span[@class='ui-icon ui-icon-circle-triangle-e']").click()
        # driver.find_element(By.XPATH,  "//div[@class='ui-datepicker-group ui-datepicker-group-last']//div[@class='ui-datepicker-header ui-widget-header ui-helper-clearfix ui-corner-right']//a[@class='ui-datepicker-next ui-corner-all']").click()

# select the first available time slot
#TODO inspect all options and select one that is closest to the preferred time slot(s)
sel = Select(driver.find_element(By.XPATH,  "//li[@id='appointments_consulate_appointment_time_input'"))
sel.select_by_index(1)
# TODO the select by index(1) function fails when there are more than 1 choice


sel.get_attribute("attribute name")

reschedule_button = driver.find_element_by_id("appointments_submit_action")
reschedule_button.click()




#### under development


# solve more than one available time selection

test = driver.find_elements(By.ID,  "appointments_consulate_appointment_time")

driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', test[0])


driver.find_element(By.XPATH,  "//a[@class='button alert']").click()

avail_field.get_attribute("class")

# check numerical record of the available dates

test = driver.find_elements(By.XPATH,  "//td[@data-handler='selectDay']")


avail_table = pd.DataFrame(columns = ['city', 'year', 'month', 'yrmth'])
if len(test)>0:

    for i in range(len(test)):
        i_mth = test[i].get_attribute("data-month")
        i_yr = test[i].get_attribute("data-year")
        i_day = test[i].text
        i_yrmth = i_yr+i_mth
        avail_table = avail_table.append({'city' : city_lkup, 'year' : i_yr, 'month' : i_mth,'yrmth' : i_yrmth}, ignore_index = True)

target_visa_appt_window = ['202201','202207']


# test finding the text of days

test = driver.find_elements(By.XPATH,  "//table[@class='ui-datepicker-calendar']")
len(test)
test[0].text


driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', test[0])



# for cycle in range(3):
#     # get all availability for specific country and visa type

#     # by-individual input
#     country_lkup = 'Canada'
#     visa_type_lkup = 'H1b'
#     city_list = ['Ottawa','Calgary','Vancouver'] #,'Halifax','Montreal','Quebec City','Toronto']
#     # time_stamp = str(datetime.datetime.now())

#     # record all availability in a table
#     avail_table = pd.DataFrame(columns = ['country','visa_type','city', 'year', 'month','day', 'yrmth'])

#     for city_lkup in city_list:
#         city_field = driver.find_element_by_id("appointments_consulate_appointment_facility_id")
#         city_field.send_keys(city_lkup)

#         avail_field = driver.find_element_by_id("appointments_consulate_appointment_date_input")
#         avail_field.click()

#         # get the all available dates in the next 24 months and write into a table
#         for m in range (8): # click the next button twice to avoid duplicated month lookup
            
#             avail_dates = driver.find_elements(By.XPATH,  "//td[@data-handler='selectDay']")

#             if len(avail_dates)>0:

#                 for i in range(len(avail_dates)):
#                     i_mth = avail_dates[i].get_attribute("data-month")
#                     i_yr = avail_dates[i].get_attribute("data-year")
#                     i_day = avail_dates[i].text
#                     i_yrmth = i_yr+i_mth
#                     avail_table = avail_table.append({'country':country_lkup,'visa_type':visa_type_lkup,'city' : city_lkup, 'year' : i_yr, 'month' : i_mth,'day' : i_day, 'yrmth' : i_yrmth}, ignore_index = True)
            
#             next_button = driver.find_element(By.XPATH,  "//div[@class='ui-datepicker-group ui-datepicker-group-last']//a[@class='ui-datepicker-next ui-corner-all']")
#             next_button.click()
#             next_button = driver.find_element(By.XPATH,  "//div[@class='ui-datepicker-group ui-datepicker-group-last']//a[@class='ui-datepicker-next ui-corner-all']")
#             next_button.click()
#             time.sleep(0.2+random.random()/10)

#             print(f'finished month {m}')

#         #reset calendar starting time
#         print(f'finished city {city_lkup}')
        
#         webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
#         time.sleep(2)

#     avail_table.to_csv(f'{avail_data_loc}avail_table_{country_lkup}_{visa_type_lkup}_{str(datetime.datetime.now())}_cycle{cycle}.csv', index = False)
    
#     time.sleep(600+random.random()*60)

# # close down the session
# driver.close()








