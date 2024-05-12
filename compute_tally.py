from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from utils import create_driver, login_admin
from config import URL_ADMIN, TIMEOUT

import time
import sys
import os
import csv


def compute_tally(driver, name_election):
    # Ir a la página web
    driver.get(f"{URL_ADMIN}/admin/{name_election}/panel")

    # Ejecuta JavaScript para realizar el scroll hasta el final de la página
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(1)

    # Abrimos el modal de iniciar elección
    compute_tally = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "compute-tally"))
    )
    compute_tally.click()

    # Presionamos el boton del modal
    button_compute_tally = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "button-compute-tally"))
    )
    button_compute_tally.click()

    WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "feedback-message"))
    )


if __name__ == "__main__":
    file_name = sys.argv[1]

    current_directory = os.path.dirname(os.path.abspath(__file__))

    driver = create_driver()
    login_admin(driver)

    # Abre el archivo CSV en modo lectura
    with open(f"{file_name}", "r") as archivo_csv:
        # Crea un lector de CSV
        lector_csv = csv.reader(archivo_csv)
        lector_csv = list(lector_csv)

        # Itera sobre cada fila del archivo CSV
        for fila in lector_csv:
            compute_tally(driver, fila[0])
