import asyncio  # Para manejar funciones asíncronas
from playwright.async_api import async_playwright  # Playwright en modo asíncrono
import sys  # Para manejar argumentos desde la línea de comandos
import os  # Para manejar rutas del sistema operativo

async def fetch_url(url, output_file):
    """
    Función para realizar scraping de una URL y guardar el contenido en múltiples formatos:
    .txt, .html, .md y una captura de pantalla en .jpg.

    Args:
        url (str): La URL de la página que se desea procesar.
        output_file (str): El nombre base del archivo donde se guardará el contenido.
    """
    # Asegurarse de que el archivo base no tenga extensión
    base_name = os.path.splitext(output_file)[0]
    
    # Construir la ruta de la carpeta "Recovered" fuera de "src"
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Ruta del proyecto
    recovered_path = os.path.join(project_root, "Recovered", base_name)
    
    # Crear la carpeta si no existe
    os.makedirs(recovered_path, exist_ok=True)
    
    # Rutas de los archivos de salida
    txt_path = os.path.join(recovered_path, f"{base_name}.txt")
    html_path = os.path.join(recovered_path, f"{base_name}.html")
    md_path = os.path.join(recovered_path, f"{base_name}.md")
    screenshot_path = os.path.join(recovered_path, f"{base_name}.jpg")

    # Iniciar Playwright en modo asíncrono
    async with async_playwright() as p:
        # Lanzar un navegador Chromium en modo headless (sin interfaz gráfica)
        browser = await p.chromium.launch(headless=True)  # Cambiar a False para depuración visual
        context = await browser.new_context()
        page = await context.new_page()

        # Configurar un User-Agent realista
        await page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        })

        # Navegar a la URL proporcionada
        await page.goto(url)

        # Esperar a que se cargue completamente la página inicial
        await page.wait_for_load_state("networkidle")

        # Simular desplazamiento para cargar contenido dinámico
        scroll_height = await page.evaluate("() => document.body.scrollHeight")
        for _ in range(10):  # Ajusta el rango según la cantidad de scrolls necesarios
            await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            await asyncio.sleep(2)  # Pausa para permitir que el contenido se cargue
            new_scroll_height = await page.evaluate("() => document.body.scrollHeight")
            if new_scroll_height == scroll_height:  # Detener si no hay más contenido
                break
            scroll_height = new_scroll_height

        # Obtener el contenido completo de la página (HTML renderizado)
        html_content = await page.content()

        # Guardar el contenido en un archivo .txt
        with open(txt_path, "w", encoding="utf-8") as file:
            file.write(html_content)

        # Guardar el contenido en un archivo .html
        with open(html_path, "w", encoding="utf-8") as file:
            file.write(html_content)

        # Guardar el contenido en un archivo .md (como texto plano)
        with open(md_path, "w", encoding="utf-8") as file:
            file.write(html_content)

        # Tomar una captura de pantalla y guardarla como .jpg
        await page.screenshot(path=screenshot_path, full_page=True)

        # Cerrar el navegador
        await browser.close()

        # Imprimir un mensaje de éxito en terminal para saber que se realizó correctamente
        print(f"Archivos generados en la carpeta:\n- {txt_path}\n- {html_path}\n- {md_path}\n- {screenshot_path}")

# Verificar si el script se ejecuta desde la línea de comandos
if __name__ == "__main__":
    # Verificar que se hayan pasado los argumentos necesarios
    if len(sys.argv) != 3:
        print("Uso: python script.py <URL> <archivo_salida>")
        sys.exit(1)
    
    # Obtener la URL y el nombre del archivo de salida desde los argumentos
    url = sys.argv[1]
    output_file = sys.argv[2]
    
    # Ejecutar la función asíncrona
    asyncio.run(fetch_url(url, output_file))