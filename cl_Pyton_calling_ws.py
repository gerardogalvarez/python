import requests
import json

def get_data():
    url = 'http://localhost:8000/api/data'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f'Error: {response.status_code}')
        return None

def update_data(new_data):
    url = 'http://localhost:8000/api/data'
    headers = {'Content-Type': 'application/json'}
    response = requests.put(url, headers=headers, data=json.dumps(new_data))
    if response.status_code == 200:
        print('Datos actualizados exitosamente.')
    else:
        print(f'Error: {response.status_code}')

def main():
    while True:
        print('1. Obtener datos')
        print('2. Actualizar datos')
        print('3. Salir')
        choice = input('Selecciona una opción: ')

        if choice == '1':
            data = get_data()
            if data:
                print('Datos:', data)
        elif choice == '2':
            new_message = input('Nuevo mensaje: ')
            update_data({'message': new_message})
        elif choice == '3':
            break
        else:
            print('Opción no válida. Por favor, selecciona una opción válida.')

if __name__ == '__main__':
    main()
