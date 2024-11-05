from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utils import create_driver, login_admin
from config import TIMEOUT, URL_ADMIN

import time
import sys
import csv
import os


def download_bundle(driver, name_election):
    # Ir a la página web
    driver.get(f"{URL_ADMIN}/admin/{name_election}/panel")

    time.sleep(1)
    # Ejecuta JavaScript para realizar el scroll hasta el final de la página
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    # Descargamos el archivo de bundle
    bundle_files_button = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='bundle-button-download']"))
    )
    bundle_files_button.click()
    time.sleep(15)


if __name__ == "__main__":
    file_name = sys.argv[1]

    bundle_directory = os.path.dirname(os.path.abspath(__file__))
    bundle_directory = os.path.join(bundle_directory, "bundle-files")

    if not os.path.exists(bundle_directory):
        os.makedirs(bundle_directory)

    # Abrimos el navegador
    driver = create_driver()
    login_admin(driver)

    # Abre el archivo CSV en modo lectura
    with open(f"{file_name}", "r") as archivo_csv:
        # Crea un lector de CSV
        lector_csv = csv.reader(archivo_csv)
        lector_csv = list(lector_csv)

        # Itera sobre cada fila del archivo CSV
        for fila in lector_csv:
            download_bundle(driver, fila[0])
