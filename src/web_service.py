from playwright.sync_api import sync_playwright  # Bibliotecas necesarias de Playwright
import sys  # Para manejar argumentos desde la línea de comandos
import os  # Para manejar rutas del sistema operativo
import time  # Para agregar pausas entre desplazamientos

def fetch_url(url, output_file):
    """
    Función para realizar scraping de una URL y guardar el contenido en un archivo .txt.
    Soporta páginas estáticas y dinámicas, incluyendo aquellas que requieren desplazamiento.

    Args:
        url (str): La URL de la página que se desea procesar.
        output_file (str): El nombre del archivo donde se guardará el contenido.

    NOTA: AÚN NO FUNCIONA CON PÁGINAS QUE REQUIEREN INICIO DE SESIÓN O CAPTCHA.
    """
    # Asegurarse de que el archivo tenga la extensión .txt
    if not output_file.endswith(".txt"):
        output_file += ".txt"
        
    # Obtener la ruta al escritorio del usuario actual
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    output_file_path = os.path.join(desktop_path, output_file)

    # Iniciar Playwright en modo síncrono
    with sync_playwright() as p:
        # Lanzar un navegador Chromium en modo headless (sin interfaz gráfica)
        browser = p.chromium.launch(headless=True)  # Cambiar a False para depuración visual
        
        # Crear un nuevo contexto de navegador con cookies habilitadas
        context = browser.new_context()
        page = context.new_page()

        # Configurar un User-Agent realista
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        })
        
        # Navegar a la URL proporcionada
        page.goto(url)
        
        # Esperar a que se cargue completamente la página inicial
        page.wait_for_load_state("networkidle")
        
        # Simular desplazamiento para cargar contenido dinámico
        scroll_height = page.evaluate("() => document.body.scrollHeight")
        for _ in range(10):  # Ajusta el rango según la cantidad de scrolls necesarios
            page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            time.sleep(2)  # Pausa para permitir que el contenido se cargue
            new_scroll_height = page.evaluate("() => document.body.scrollHeight")
            if new_scroll_height == scroll_height:  # Detener si no hay más contenido
                break
            scroll_height = new_scroll_height
        
        # Obtener el contenido completo de la página (HTML renderizado)
        html_content = page.content()
        
        # Guardar el contenido en un archivo .txt en el escritorio 
        # (Que definimos anteriormente en output_file_path, pero lo podemos cambiar a cualquier directorio)
        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(html_content)
        
        # Cerrar el navegador
        browser.close()

        # Imprimir un mensaje de éxito en terminal para saber que se realizó correctamente
        print(f"El contenido de la página {url} se ha guardado en {output_file_path}.")

# Verificar si el script se ejecuta desde la línea de comandos
if __name__ == "__main__":
    # Verificar que se hayan pasado los argumentos necesarios
    if len(sys.argv) != 3:
        print("Uso: python script.py <URL> <archivo_salida>")
        sys.exit(1)
    
    # Obtener la URL y el nombre del archivo de salida desde los argumentos
    url = sys.argv[1]
    output_file = sys.argv[2]
    
    # Llamar a la función para procesar la URL
    fetch_url(url, output_file)