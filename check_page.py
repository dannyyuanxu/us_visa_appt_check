# this script opens up page and check available dates location

#### set up
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome

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

city_field = driver.find_element_by_name("appointments[consulate_appointment][facility_id]")
city_field.send_keys("Ottawa")


avail_field = driver.find_element_by_id("appointments_consulate_appointment_date_input")
avail_field.click()



#### under development

while True:
    try:
        print("start trying to click")
        wait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, "//td[@data-handler='selectDay']"))).click()
    except:
        print("move to next page")
        driver.find_element(By.XPATH,  "//div[@class='ui-datepicker-group ui-datepicker-group-last']//div[@class='ui-datepicker-header ui-widget-header ui-helper-clearfix ui-corner-right']//a[@class='ui-datepicker-next ui-corner-all']").click()

# date_list = driver.find_elements(By.XPATH, '//table[@td class=" undefined"]')

# if len(date_list)>0:
#     date_list[0].click()

# date_list = driver.find_elements(By.XPATH, '//table[@td class=" undefined"]')










# close down the session
driver.close()
