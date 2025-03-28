# AccessibilityTool - Fase 1: Scraping

La primera fase de este proyecto realiza Web Scraping para obtener el contenido de páginas web estáticas y dinámicas, y guardarlo en un archivo `.txt` en el escritorio del usuario.

## ¿Qué hace este script?
- Navega a una URL proporcionada.
- Carga contenido dinámico generado por JavaScript.
- Simula desplazamiento (scroll) para cargar más contenido.
- Guarda el contenido HTML en un archivo `.txt` en tu escritorio.

## Requisitos
1. **Python 3.7 o superior**.
2. Instalar las dependencias:
   ```
   pip install playwright
   playwright install
   ```

## Cómo usarlo
1. Ejecuta el script desde la terminal:
   ```
   python src/web_service.py "URL" "nombre_archivo"
   ```
   - **URL**: La página web que deseas scrapear.
   - **nombre_archivo**: Nombre del archivo (sin `.txt`).

2. El archivo se guardará en tu escritorio como `nombre_archivo.txt`.

## Ejemplo
```bash
python src/web_service.py "https://uv.mx" "UV"
```
Esto guardará el contenido de `https://uv.mx` en un archivo llamado `UV.txt` en tu escritorio.

## Notas
- Si la página bloquea el scraping, intenta usar un proxy o habilitar cookies, aunque en las pruebas no funciona aún con páginas con algún tipo de protección al estilo CloudFront o similares.
- Cambia `headless=True` a `headless=False` en el código para ver el navegador en acción.