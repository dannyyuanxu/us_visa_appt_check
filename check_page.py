# this script opens up page and check available dates location

#### set up
import yaml
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
import dotenv

# read in config
with open('config.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    config = yaml.load(file, Loader=yaml.FullLoader)

login_site = config["reschedule_web"]

# read in environment variable
dotenv.load_dotenv()
login_username = os.getenv('USERNAME')
login_password = os.getenv('PASSWORD')




#### webpage operations

# open a browser
driver = webdriver.Chrome(ChromeDriverManager().install())
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

# select



# close down the session 
driver.close()
