from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Ruta para la raíz que muestra un mensaje simple
@app.route('/')
def home():
    return "Bienvenido al servicio de scraping:) - Usa /fetch para recuperar una página web."

# Definir una ruta para el servicio web que puede ser invocada mediante GET o POST
@app.route('/fetch', methods=['GET', 'POST'])
def fetch_page():
    # Obtener la URL del parámetro de la solicitud
    url = request.args.get('url') if request.method == 'GET' else request.form.get('url')
    
    # Verificar si la URL está presente
    if not url:
        return jsonify({"error": "Falta el parámetro de URL"}), 400

    try:
        # Realizar una solicitud GET a la URL proporcionada
        response = requests.get(url)
        response.raise_for_status()
        
        # Usar BeautifulSoup para analizar el contenido HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraer el contenido deseado (por ejemplo, el título de la página)
        page_title = soup.title.string if soup.title else "No se encontró título"
        
        # Devolver el contenido de la página web en formato JSON
        return jsonify({"title": page_title, "content": response.text}), 200
    except requests.RequestException as e:
        # Manejar errores de la solicitud
        return jsonify({"error": str(e)}), 500