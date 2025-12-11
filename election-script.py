import requests
import base64
import json
import sys
import aiohttp
import asyncio

BACKEND_URL = 'http://localhost:8000'
USER = 'admin'
PASSWORD = '12345'

election_file = "election.json"

try:

    encoded = base64.b64encode(f"{USER}:{PASSWORD}".encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded}',
        'Content-Type': 'application/json'
    }

    response = requests.post(f'{BACKEND_URL}/login', headers=headers)
    token = response.json()['token']

except Exception as e:
    print(f'Error en el login: {e}')

def create_election(election_data):
    try:
        headers['Authorization'] = f'Bearer {token}'
        response = requests.post(f'{BACKEND_URL}/create-election', headers=headers, json=election_data)
        if response.status_code != 201:
            raise Exception(response)

        return election_data["short_name"]
    except Exception as e:
        print(f'Error al crear la elección: {e}')
        return None

def add_questions(election_name, questions):
    try:
        headers['Authorization'] = f'Bearer {token}'
        response = requests.post(f'{BACKEND_URL}/create-questions/{election_name}', 
            headers=headers, 
            json={
                'question': questions
            }
        )
        if response.status_code != 200:
            raise Exception(response)
    except Exception as e:
        print(f'Error al agregar preguntas: {e}')
        return False
    
def add_trustee(election_name, trustee_data):
    try:
        headers['Authorization'] = f'Bearer {token}'
        response = requests.post(f'{BACKEND_URL}/{election_name}/create-trustee', headers=headers, json=trustee_data)
        if response.status_code != 200:
            raise Exception(response)
    except Exception as e:
        print(f'Error al agregar trustee: {e}')
        return False
    
async def add_voters(election_name, voters_file):
    try:
        headers['Authorization'] = f'Bearer {token}'
        data = aiohttp.FormData()
        data.add_field('file', 
                      open(voters_file, 'r'),
                      filename=voters_file.split('/')[-1])
        
        async with aiohttp.ClientSession() as session:
            url = f"{BACKEND_URL}/{election_name}/upload-voters"
            async with session.post(url, headers=headers, data=data) as resp:
                if resp.status != 200:
                    raise Exception(await resp.text())
    except Exception as e:
        print(f'Error al agregar votantes: {e}')
        return False
    
def start_election(election_name):
    try:
        headers['Authorization'] = f'Bearer {token}'
        response = requests.post(f'{BACKEND_URL}/{election_name}/start-election', headers=headers)
        if response.status_code != 200:
            raise Exception(response.json())
    except Exception as e:
        print(f'Error al iniciar la elección: {e}')
        return False
    
def end_election(election_name):
    try:
        headers['Authorization'] = f'Bearer {token}'
        response = requests.post(f'{BACKEND_URL}/{election_name}/end-election', headers=headers)
        if response.status_code != 200:
            raise Exception(response.json())
    except Exception as e:
        print(f'Error al cerrar la elección: {e}')
        return False
    
def compute_tally(election_name):
    try:
        headers['Authorization'] = f'Bearer {token}'
        response = requests.post(f'{BACKEND_URL}/{election_name}/compute-tally', headers=headers)
        if response.status_code != 200:
            raise Exception(response)
    except Exception as e:
        print(f'Error al computar el conteo: {e}')
        return False
    
def release_results(election_name):
    try:
        headers['Authorization'] = f'Bearer {token}'
        response = requests.post(f'{BACKEND_URL}/{election_name}/results-release', headers=headers)
        if response.status_code != 200:
            raise Exception(response)
    except Exception as e:
        print(f'Error al liberar los resultados: {e}')
        return False

def delete_election(election_name):
    try:
        headers['Authorization'] = f'Bearer {token}'
        response = requests.get(f'{BACKEND_URL}/delete-election/{election_name}', headers=headers)
        if response.status_code != 200:
            raise Exception(response)
    except Exception as e:
        print(f'Error al eliminar elección: {e}')
        return False
    
async def config_election(elections):

    for election in elections:
        election_name = create_election(election)
        add_questions(election_name, election['questions'])
        add_trustee(election_name, election['trustees'])
        voters_file = election['voters_file']
        await add_voters(election_name, voters_file)

def start_elections(elections):
    for election in elections:
        election_name = election['short_name']
        start_election(election_name)

def end_elections(elections):
    for election in elections:
        election_name = election['short_name']
        end_election(election_name)

def compute_tally_elections(elections):
    for election in elections:
        election_name = election['short_name']
        compute_tally(election_name)

def release_elections_results(elections):
    for election in elections:
        election_name = election['short_name']
        release_results(election_name)

def delete_elections(elections):
    for election in elections:
        election_name = election['short_name']
        delete_election(election_name)
       
async def main():
    try:
        with open(election_file, 'r') as file:
            election_data = json.load(file)
            elections = election_data['elections']

        operations = {
            'config': config_election,
            'start': start_elections,
            'end': end_elections,
            'tally': compute_tally_elections,
            'release': release_elections_results,
            'delete': delete_elections
        }

        operation = sys.argv[1]
        if operation not in operations:
            print(f'Operación no válida: {operation}')
            sys.exit(1)

        if asyncio.iscoroutinefunction(operations[operation]):
            await operations[operation](elections)
        else:
            operations[operation](elections)

    except Exception as e:
        print(f'Error en la ejecución: {e}')

if __name__ == '__main__':
    asyncio.run(main())
