from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from config import TIMEOUT, NAME
from login_oauth import login_oauth

import sys
import os
import csv
import time


def trustee_decrypt(drive, name_election):
    login_oauth(driver, name_election)

    # Accedemos a la etapa 3
    button_decrypt = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "upload-key"))
    )
    button_decrypt.click()

    # Subimos el archivo
    drop_zone = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "file-input"))
    )
    drop_zone.send_keys(os.path.abspath(f"trustee_key_{NAME}_{name_election}.txt"))

    # Esperamos a que el proceso se complete
    feedback = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "feedback-message-2"))
    )
    time.sleep(1)


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
            trustee_decrypt(driver, fila[0])
