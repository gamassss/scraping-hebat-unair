from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

service = ChromeService(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service)

driver.get("https://hebat.elearning.unair.ac.id/")

login_button = driver.find_element(By.CSS_SELECTOR, "a.login-open")
login_button.click()

username_field = driver.find_element(By.NAME, "username")
username_field.send_keys("YOUR_NIM")
password_field = driver.find_element(By.NAME, "password")
password_field.send_keys("YOUR_PASSWORD")

login_form = driver.find_element(By.ID, "header-form-login")
login_form.submit()
