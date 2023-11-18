'''webapi_callback_finishing module'''
import os
import time
import datetime
from flask import Flask, request, jsonify
import requests

TOKEN_EXPIRING_TIME = None
TOKEN = None

app = Flask(__name__)


def refresh_token():
    ''' Get a new/fresh token '''
    # Obtén la hora actual
    hora_actual = datetime.datetime.now()

    global TOKEN, TOKEN_EXPIRING_TIME

    # Verifica si la var. token es vacía o si TOKEN_EXPIRING_TIME es menor o igual a la hora actual
    if not TOKEN or not TOKEN_EXPIRING_TIME or TOKEN_EXPIRING_TIME <= hora_actual:
        url = "https://stg-identity.primaverabss.com/connect/token"

        payload = 'grant_type=client_credentials&client_id=finishing-csu-tests&client_secret=iXq9EzrlMQerXCil8gDS0BigUEWHZIrmEdNNd7BAvkYdFvb0Y9uBYthLp6nMYsztXghduJcYHQhBGKXYAXUfcw22'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload, timeout=30)

        TOKEN = response.json()["access_token"]

        expires_in = response.json()["expires_in"]

        TOKEN_EXPIRING_TIME = hora_actual + datetime.timedelta(seconds=expires_in)

        print (f'Nuevo token: {TOKEN}')
        print (f'Nuevo TOKEN_EXPIRING_TIME: {TOKEN_EXPIRING_TIME}')

    return TOKEN


def process_callback(payload):
    ''' This is the callback processing function '''

    # Aquí puedes realizar el procesamiento adicional según tus necesidades
    document_type = payload['data']['documentType']
    process_id = payload['id']
    print(f"Recibido callback para documento tipo: {document_type}")

    current_token = refresh_token()

    headers = {
        'Accept-Language': 'es-ES',
        'Authorization': f'Bearer {current_token}'
    }

    # Realiza la llamada GET a la URL especificada
    try:
        url = f"https://st-dfs.lithium.primaverabss.com/api/v1/PRIMAVERA/CSU01-PRIMAVERACSU010001/finishing/processes/{process_id}/file"
        response = requests.get(url, headers=headers, timeout = 30)

        create_pdf_file(response.content)

        # Aquí puedes procesar la respuesta según tus necesidades
        print(f"Llamada GET a {url}. Estado de la respuesta: {response.status_code}")
    except Exception as e:
        print(f"Error al realizar la llamada GET: {str(e)}")

def create_pdf_file(content):
    ''' Generates PDF file '''
    file_extension = 'pdf'
    file_name = 'temp-finishing-' +  str(time.time()) + '.' + file_extension
    file_path = os.path.join(os.getcwd(), file_name)
    print(file_path)
    with open(file_path, 'wb') as f:
        f.write(content)

@app.route('/callback', methods=['POST'])
def callback():
    '''This is the callback endpoint: POST'''
    try:
        payload = request.json['payload']
        
        process_callback(payload)

        return jsonify({'success': True}), 200
    except Exception as e:
        print (f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':

    app.run(debug=True)
