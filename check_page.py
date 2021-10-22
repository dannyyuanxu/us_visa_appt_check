# this script opens up page and check available dates location

#### set up
import pandas as pd
import yaml
# from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from selenium.webdriver.support.select import Select

import os
import dotenv

# read in config
with open('config.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    config = yaml.load(file, Loader=yaml.FullLoader)

login_site = config["reschedule_web"]

# read in environment variables
dotenv.load_dotenv()
login_username = os.getenv('USERNAME')
login_password = os.getenv('PASSWORD')


#### webpage operations

# open a browser
driver = Chrome()

# altenative way
# from webdriver_manager.chrome import ChromeDriverManager
# driver = webdriver.Chrome(ChromeDriverManager().install())



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

# test out one city

city_list = ['Ottawa','Calgary','Vancouver','Halifax','Montreal','Quebec City','Toronto']
city_lkup = city_list[0]
city_field = driver.find_element_by_name("appointments[consulate_appointment][facility_id]")
city_field.send_keys(city_lkup)


avail_field = driver.find_element_by_id("appointments_consulate_appointment_date_input")
avail_field.click()

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
sel = Select(driver.find_element(By.ID,  "appointments_consulate_appointment_time"))
sel.select_by_index (1)

sel.get_attribute("attribute name")

reschedule_button = driver.find_element_by_id("appointments_submit_action")
reschedule_button.click()


#### under development


driver.find_element(By.XPATH,  "//a[@class='button alert']").click()

avail_field.get_attribute("class")


# if len(date_list)>0:
#     date_list[0].click()

# date_list = driver.find_elements(By.XPATH, '//table[@td class=" undefined"]')

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


# close down the session
driver.close()
