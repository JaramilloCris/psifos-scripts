from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from utils import login_admin, create_driver
from config import URL_ADMIN, TIMEOUT, TRUSTEE_NAME_1, TRUSTEE_NAME_2, TRUSTEE_NAME_3, TRUSTEE_ID_1, TRUSTEE_ID_2, TRUSTEE_ID_3, TRUSTEE_EMAIL_1, TRUSTEE_EMAIL_2, TRUSTEE_EMAIL_3

import time
import csv
import os
import sys
import json


def config_election(driver, data_election):
    # Ir a la página web
    driver.get(f"{URL_ADMIN}/admin/home")

    short_name_election = data_election["short_name"]
    name_election = data_election["name"]
    description_election = data_election["description"]
    file_voters = data_election["file_voters"]
    file_questions = data_election["file_questions"]

    # Accedemos a crear una elección
    button_create = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "button-create-election"))
    )
    button_create.click()

    # Completamos los formularios
    short_name_input = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "input-short-name"))
    )
    short_name_input.send_keys(short_name_election)

    name_input = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "input-name"))
    )
    name_input.send_keys(name_election)

    description_input = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.CLASS_NAME, "textarea"))
    )
    description_input.send_keys(description_election)

    # Ejecuta JavaScript para realizar el scroll hasta el final de la página
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(1)

    # Marcamos en 1 el peso de la elección
    weight_input = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='weight-input']"))
    )
    weight_input.clear()
    weight_input.send_keys("8")

    # Normalizar resultados
    normalize_input = WebDriverWait(driver, TIMEOUT).until(
     EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/section[2]/div/div[10]/div/label/input"))
    )
    normalize_input.click()

    # Enviamos los datos para crear
    button_send = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='button-send-election']"))
    )
    button_send.click()
    time.sleep(1)

    # Esperamos a la pantalla de inicio
    WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "election-subtitle"))
    )

    add_trustee(
        driver, short_name_election, TRUSTEE_NAME_1, TRUSTEE_ID_1, TRUSTEE_EMAIL_1
    )
    add_trustee(
        driver, short_name_election, TRUSTEE_NAME_2, TRUSTEE_ID_2, TRUSTEE_EMAIL_2
    )
    add_trustee(
        driver, short_name_election, TRUSTEE_NAME_3, TRUSTEE_ID_3, TRUSTEE_EMAIL_3
    )

def upload_voters(driver, name_election, file_name):
    # Ir a la página web
    driver.get(f"{URL_ADMIN}/admin/{name_election}/panel")

    time.sleep(1)
    # Ejecuta JavaScript para realizar el scroll hasta el final de la página
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    # Abrimos el modal de subir votantes
    button_add = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='button-add-voters']"))
    )
    button_add.click()

    # Subimos el archivo
    file_input = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "fileinput"))
    )
    file_input.send_keys(os.path.abspath(file_name))

    # Presionamos el boton del modal
    button_upload_voters = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "button-upload-voters"))
    )
    button_upload_voters.click()

    # Esperamos que termine el proceso
    feedback = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "feedback-upload"))
    )


def add_trustee(driver, name_election, name_trustee, login_id, trustee_email):
    # Ir a la página web
    driver.get(f"{URL_ADMIN}/admin/{name_election}/trustee")

    # Entramos al formulario del custodio
    button_trustee = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "add-trustee"))
    )
    button_trustee.click()

    button_trustee_modal = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "next-trustee"))
    )
    button_trustee_modal.click()

    # Rellenamos el formulario del custodio
    trustee_name_input = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "trustee-name"))
    )
    trustee_name_input.send_keys(name_trustee)

    trustee_id_input = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "trustee-id"))
    )
    trustee_id_input.send_keys(login_id)

    trustee_email_input = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "trustee-email"))
    )
    trustee_email_input.send_keys(trustee_email)

    # Enviamos la información del custodio
    send_trustee = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "send-trustee"))
    )
    send_trustee.click()
    time.sleep(1)


def add_question(driver, question, question_number):
    max_options = question.get("max_options", 1)

    # Completamos los formularios
    add_question = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='add-question']"))
    )
    add_question.click()

    name_input = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, f"//*[@id='name-{question_number}']"))
    )
    name_input.send_keys(f"{question['question']}")

    input_max_options = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//*[@id='question-{question_number}-max-answers']")
        )
    )

    input_max_options.clear()
    input_max_options.send_keys(f"{max_options}")

    # Enviamos los datos para crear
    button_add_option = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//*[@id='add-option-{question_number}']")
        )
    )

    for index_answer, answer in enumerate(question["answers"]):
        # Ejecuta JavaScript para realizar el scroll hasta el final de la página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(1)
        button_add_option.click()

        # Esperamos a la pantalla de inicio
        input_option = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"//*[@id='question-{question_number}-text-option-{index_answer}']",
                )
            )
        )
        for c in answer:
            input_option.send_keys(f"{c}")
        for c in answer:
            input_option.send_keys(f"{c}")


def create_questions(driver, name_election, file_name):
    # Ir a la página web
    driver.get(f"{URL_ADMIN}/admin/{name_election}/panel")

    time.sleep(1)
    # Ejecuta JavaScript para realizar el scroll hasta el final de la página
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    # Accedemos a crear preguntas
    button_create_question = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='button-add-questions']"))
    )
    button_create_question.click()

    # Lee el archivo JSON
    with open(f"{file_name}", "r") as f:
        questions = json.load(f)

    for index, question in enumerate(questions):
        add_question(driver, question, index + 1)

    save_question = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='button-save-questions']"))
    )
    save_question.click()
    time.sleep(1)

    # Esperamos a la pantalla de inicio
    WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='election-subtitle']"))
    )


if __name__ == "__main__":
    file_name = sys.argv[1]
    driver = create_driver()

    login_admin(driver)

    # Abre el archivo CSV en modo lectura
    with open(f"{file_name}", "r") as archivo_csv:
        # Crea un lector de CSV
        lector_csv = csv.reader(archivo_csv)
        lector_csv = list(lector_csv)

        # Itera sobre cada fila del archivo CSV
        for fila in lector_csv:
            data_election = {
                "short_name": fila[0],
                "name": fila[1],
                "description": fila[2],
                "file_voters": fila[3],
                "file_questions": fila[4],
            }
            config_election(driver, data_election)
            if fila[3] != "":
                upload_voters(driver, data_election["short_name"], fila[3])
            if fila[4] != "":
                create_questions(driver, data_election["short_name"], fila[4])
