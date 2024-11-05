import requests
import time
import csv
import json
import sys

# URL_PUBLIC = "https://participa.uchile.cl/psifos/api/public"


# def get_voters(voters):
#     ret = []
#     for v in voters["voters"]:
#         if v["cast_vote"] is not None:
#             ret.append(v["voter_login_id"])
#             print(v["voter_name"])
#     return ret


# elections = []
# file_name = sys.argv[1]
# with open(f"{file_name}", "r") as archivo_csv:
#     # Crea un lector de CSV
#         lector_csv = csv.reader(archivo_csv)
#         lector_csv = list(lector_csv)

#         # Itera sobre cada fila del archivo CSV
#         for fila in lector_csv:
#             elections += [fila[0]]

# elections_voters = []
# for election in elections:
#     if "medicina" in election:
#         page_size = 180
#     elif "facso" in election:
#         page_size = 60
#     else:
#         page_size = 51
#     votes_json = requests.post(f"{URL_PUBLIC}/election/{election}/votes", json={"page_size": page_size}).json()
#     time.sleep(3)
#     valid_voters = get_voters(votes_json)
    # elections_voters += valid_voters

elections_voters = ["waguilar", "pjbustamante", "carayac", "gonzalocabrera", "mcano", "taniaalfaro", "lefio.celedon", "monica.acuna", "gcarrasco", "valiaga", "juansalas", "zitaandrade", "scastillop", "jeleiva", "mmontt", "german.bass", "calvarez8", "jchnaiderman", "melopez", "carriagada", "fberlagoscky", "fsalazar", "rilopez", "lcifuent", "sburgos", "cleber.cirineu", "bsuarez", "angela", "wapt", "pasore", "rodrigosepulveda", "alba.lozano", "rodrigotorres", "ccollado", "mamella", "ptron001", "cacuellar", "jenan.mohammad", "uurzua", "gcuellar", "mcmolinas", "mdelafue", "cvalenzu", "mvillagran", "german.hermosilla", "izulanta", "lherrera", "fdelpino", "mdiaz", "degana", "mespinoza", "alefuentes", "igalaz2009", "mgalindo", "pagalvez", "mgoldsack", "patricia.grau", "pamelagutierrez", "mauricioh", "gabrielahuepe", "ljara", "njuretic", "ukemmerling", "nlagos", "roxanalara", "rodolfo.morrison", "claudiamunoz", "aocampo", "edopazo", "oorellan", "jortizc", "carlososorio", "drparra", "mpenna", "ipepper", "dquijada", "mirliana", "jame.rebolledo", "pfriquelme", "rrodriguezg", "xrojas", "lromero", "jeromero", "paruiz", "pabloruizr", "vsabaj"]

api = "https://api.uchile.cl/v1/personas/pasaportes?usuario=%s"
headers = {'AppKey': 'UJVQs5sw33svXNt', 'Origin': 'https://appexternal-example-desa.uchile.cl',
           'cache-control': 'no-cache'}

m = 0
out = {"MASC": 0, "FEME": 0}

while True:
    data = ""
    for voter in elections_voters[m:m + 50]:
        data += "\"" + voter + "\","
    print(data)
    resp = requests.get(api % data, headers=headers)
    response_data = json.loads(resp.content.decode('utf-8'))
    for persona in response_data['data']['getRowsPersona']:
        g = persona['genero']
        if "MASCULINO" in g:
            out["MASC"] += 1
        elif "FEMENINO" in g:
            out["FEME"] += 1
    if m + 50 > len(elections_voters):
        break
    else:
        m = m + 50
    
print(out)
