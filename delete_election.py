from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from utils import login_admin
from config import TIMEOUT, URL_ADMIN

import time
import sys
import csv
import os


def init_election(driver, name_election):
    # Ir a la página web
    driver.get(f"{URL_ADMIN}/admin/{name_election}/panel")

    time.sleep(1)
    # Ejecuta JavaScript para realizar el scroll hasta el final de la página
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    # Abrimos el modal de borrar elección
    delete_election = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id=\"accordion-section\"]/div/div[2]/div[1]/div[1]/div[2]/div[7]/a"))
    )
    delete_election.click()

    # Presionamos el boton del modal
    button_delete_election = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[8]/div[2]/footer/div/button[2]"))
    )
    button_delete_election.click()

    
    # Presionamos el boton del modal
    button_back = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[8]/div[2]/footer/div/button"))
    )
    button_back.click()


if __name__ == "__main__":
    file_name = sys.argv[1]

    current_directory = os.path.dirname(os.path.abspath(__file__))

    options = webdriver.ChromeOptions()
    options.add_argument("--private")
    prefs = {"download.default_directory": current_directory}
    options.add_experimental_option("prefs", prefs)

    # Abrimos el navegador
    driver = webdriver.Chrome(options=options)
    login_admin(driver)

    # Abre el archivo CSV en modo lectura
    with open(f"{file_name}", "r") as archivo_csv:
        # Crea un lector de CSV
        lector_csv = csv.reader(archivo_csv)
        lector_csv = list(lector_csv)

        # Itera sobre cada fila del archivo CSV
        for fila in lector_csv:
            init_election(driver, fila[0])
