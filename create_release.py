import os
import requests
import datetime

# Obtenemos el token desde las variables de entorno de Jenkins
github_token = os.getenv('GITHUB_TOKEN')

# Configuración del repositorio
repo_owner = 'msidliare'  # Cambia por tu nombre de usuario de GitHub
repo_name = 'Random_C'  # Cambia por el nombre de tu repositorio
release_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/releases'

# Obtener la fecha y hora actual para el nombre del tag y release
current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
tag_name = f'v{current_time}'  # Formato: vYYYY-MM-DD_HH-MM-SS
release_name = f'Release {current_time}'

# Ruta al archivo ejecutable generado
executable_file_path = './random_c_program'  # Asegúrate de que la ruta sea correcta

# Crear la release en GitHub
headers = {
    'Authorization': f'token {github_token}',
    'Accept': 'application/vnd.github.v3+json'
}

# Datos para crear la release
release_data = {
    'tag_name': tag_name,
    'name': release_name,
    'body': f'Release generada automáticamente el {current_time}',
    'draft': False,  # No será un borrador
    'prerelease': False  # No es una prerelease
}

response = requests.post(release_url, json=release_data, headers=headers)
release_info = response.json()

if response.status_code == 201:
    print(f'Release creada correctamente: {release_info["html_url"]}')
    upload_url = release_info['upload_url'].split('{')[0]  # URL para subir archivos

    # Subir el ejecutable a la release
    with open(executable_file_path, 'rb') as file:
        files = {
            'file': ('random_c_program', file, 'application/octet-stream')
        }
        upload_response = requests.post(
            upload_url + f'?name=random_c_program&label={tag_name}',
            headers={'Authorization': f'token {github_token}'},
            files=files
        )

    if upload_response.status_code == 201:
        print('Archivo subido correctamente a la release.')
    else:
        print(f'Error al subir el archivo: {upload_response.status_code}')
else:
    print(f'Error al crear la release: {response.status_code} - {response.text}')
