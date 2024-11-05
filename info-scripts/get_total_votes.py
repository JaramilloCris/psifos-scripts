import requests
import time
import csv
import json
import sys

URL_PUBLIC = "https://psifos-participa.uchile.cl/psifos/api/public"

elections = []
file_name = sys.argv[1]
unit = sys.argv[2]
with open(f"{file_name}", "r") as archivo_csv:
    # Crea un lector de CSV
        lector_csv = csv.reader(archivo_csv)
        lector_csv = list(lector_csv)

        # Itera sobre cada fila del archivo CSV
        for fila in lector_csv:
            elections += [fila[0]]

elections_json = []
for election in elections:
    election_json = requests.get(f"{URL_PUBLIC}/election/{election}").json()
    elections_json += [election_json]

# elections = requests.post(f"{URL_PUBLIC}/elections")
# elections_json = elections.json()

cantidad_votos = [["NOMBRE LARGO", "VOTOS RECIBIDOS", "TOTAL PADRÓN"]]
por_candidatos = []


for election in elections_json:
    election_short_name = election["short_name"]
    election_name = election["name"]
    election_result = json.loads(election["result"]) if election["result"] else None
    election_questions = election["questions"]
    election_questions = json.loads(election_questions) if election_questions else None
    stats_request = requests.get(
        f"{URL_PUBLIC}/get-election-stats/{election_short_name}"
    )
    stats_json = stats_request.json()
    num_casted_votes = stats_json["num_casted_votes"]
    total_voters = stats_json["total_voters"]

    cantidad_votos.append([election_name, num_casted_votes, total_voters])

    if election_result:
        for question in election_questions:
            results = [election_name] + election_result[0]["ans_results"]
            por_candidatos.append(
                [
                    results,
                ]
            )

    time.sleep(1)


# Abrir el archivo CSV en modo escritura
with open("cantidad_votos_%s.csv" % unit, "w", newline="") as archivo_csv:
    # Crear un escritor CSV
    escritor_csv = csv.writer(archivo_csv)

    # Escribir los datos en el archivo CSV
    for fila in cantidad_votos:
        escritor_csv.writerow(fila)


# Abrir el archivo CSV en modo escritura
with open("por_candidato.csv", "w", newline="") as archivo_csv:
    # Crear un escritor CSV
    escritor_csv = csv.writer(archivo_csv)

    # Escribir los datos en el archivo CSV
    for election in por_candidatos:
        for fila in election:
            escritor_csv.writerow(fila)
