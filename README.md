# TP: Desarrollo de Aplicación Web SPA - Dietética "Vida Equilibrada"

## Arquitectura y Tecnologías
* **Backend:** Python con Flask + Flasgger (Documentación de API).
* **Frontend:** SPA con HTML5, CSS3 y Vanilla JavaScript (sin frameworks).
* **Base de Datos:** SQLite para persistencia local.
* **Pruebas:** `unittest` para lógica de API y `Playwright` para pruebas E2E.

## Dificultades y Soluciones
1. **Entorno de ejecución:** Hubo problemas de rutas con el entorno virtual. Se solucionó activándolo correctamente con `.\.venv\Scripts\Activate.ps1` para usar las dependencias locales.
2. **Renderizado de productos:** Las "cards" no cargaban por la caché del navegador y funciones duplicadas en JS. Se solucionó forzando la recarga y depurando el código.
3. **Sincronización del DOM:** El contador del carrito presentaba desfasajes. Se centralizó la carga de datos para reflejar fielmente el estado del backend en tiempo real.
4. **Tests E2E:** Las pruebas daban `TimeoutError` por los tiempos de carga asíncronos. Se implementó `wait_for_function` para que el script espere dinámicamente la actualización de la interfaz.
5. **Persistencia:** Para evitar errores de ruta en el servidor de producción, se implementó `os.path.join` garantizando siempre la ruta absoluta de la base de datos.

## Ejecución local
1. Activar el entorno: `.\.venv\Scripts\Activate.ps1`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ejecutar la API: `python api_dietetica.py`
4. Acceder en el navegador a: `http://127.0.0.1:5000`

## Deploy
El proyecto está desplegado en **Render**, plataforma que permite ejecutar el servidor de Python junto a SQLite.
