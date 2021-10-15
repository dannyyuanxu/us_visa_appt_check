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

login_site = config["login_site"]

# read in environment variable
dotenv.load_dotenv()
login_username = os.getenv('USERNAME')
login_password = os.getenv('PASSWORD')

#### webpage operations

driver = webdriver.Chrome(ChromeDriverManager().install())
# with  webdriver.Chrome(ChromeDriverManager().install())() as driver:
    #your code inside this indent

# open page and log in
driver.get(login_site)

username_field = driver.find_element_by_name("user[email]")
username_field.clear()
username_field.send_keys(login_username)

password_field = driver.find_element_by_name("user[password]")
password_field.clear()
password_field.send_keys(login_password)


# under development:

# policy_check = driver.find_element_by_name("policy_confirmed").click()

policy_check = driver.find_element_by_xpath("//input[@id='policy_confirmed']")

policy_check.click()

browser.find_element_by_id("15 Minute Stream Flow Data: USGS (FIFE)").click()