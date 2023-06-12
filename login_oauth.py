from config import URL_ADMIN, TIMEOUT
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from config import NAME, PASSWORD


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
