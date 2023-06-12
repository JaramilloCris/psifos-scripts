from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from login_oauth import login_oauth
from config import TIMEOUT, NAME

import os
import csv
import sys
import time


def trustee_generator_key(driver, name_election):
    login_oauth(driver, name_election)
    # Accedemos a la etapa 1
    button_key_generator = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "init-key-generator"))
    )
    button_key_generator.click()

    # Descargamos la key
    button_download_key = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "download-key"))
    )
    button_download_key.click()

    time.sleep(3)

    # Subimos el archivo
    drop_zone = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "file-input"))
    )
    drop_zone.send_keys(os.path.abspath(f"trustee_key_{NAME}_{name_election}.txt"))

    finish = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "button-init"))
    )


if __name__ == "__main__":
    file_name = sys.argv[1]

    current_directory = os.path.dirname(os.path.abspath(__file__))

    options = webdriver.ChromeOptions()
    options.add_argument("--private")
    prefs = {"download.default_directory": current_directory}
    options.add_experimental_option("prefs", prefs)

    # Abrimos el navegador
    driver = webdriver.Chrome(options=options)

    # Abre el archivo CSV en modo lectura
    with open(f"{file_name}", "r") as archivo_csv:
        # Crea un lector de CSV
        lector_csv = csv.reader(archivo_csv)
        lector_csv = list(lector_csv)

        # Itera sobre cada fila del archivo CSV
        for fila in lector_csv:
            trustee_generator_key(driver, fila[0])
