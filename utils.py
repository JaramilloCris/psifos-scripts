from config import URL_ADMIN, TIMEOUT
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from config import NAME, PASSWORD, URL_ADMIN, ADMIN_PASSWORD, ADMIN_USER
from selenium import webdriver

import os


def create_driver(download_directory=os.getcwd()):
    service = Service(executable_path='./chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument("--private")
    prefs = {"download.default_directory": download_directory}
    options.add_experimental_option("prefs", prefs)

    return webdriver.Chrome(service=service, options=options)


def login_admin(driver):
    # Ir a la página web
    driver.get(URL_ADMIN)

    # Encontrar y completar el formulario de inicio de sesión
    username_element = driver.find_element("id", "user-login")
    username_element.send_keys(ADMIN_USER)

    password_element = driver.find_element("id", "clave-login")
    password_element.send_keys(ADMIN_PASSWORD)

    submit_element = driver.find_element(By.CLASS_NAME, "footer-register-button")
    submit_element.click()

    WebDriverWait(driver, 15000).until(
        EC.presence_of_element_located((By.ID, "election-subtitle"))
    )

def login_oauth(driver, name_election):
    # Ir a la página web
    driver.get(f"{URL_ADMIN}/api/app/{name_election}/trustee/login")

    username_element_id = "usernameInput"
    password_element_id = "passwordInput"

    # Rellenamos el formulario del custodio
    name_input = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, username_element_id))
    )
    name_input.send_keys(NAME)

    password_input = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, password_element_id))
    )
    password_input.send_keys(PASSWORD)

    password_input.send_keys(Keys.ENTER)
