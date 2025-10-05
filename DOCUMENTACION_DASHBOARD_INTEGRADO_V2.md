# Documentación del Dashboard Rohayhu Celebra! (Versión Integrada y Desplegable)

## 1. Introducción

Este documento detalla la implementación de un dashboard web completo para la automatización de "Rohayhu Celebra!". La aplicación permite generar enlaces personalizados para regalos digitales (videos, audios, PDFs, enlaces externos) y enviar correos electrónicos profesionales a los destinatarios, todo desde una interfaz web intuitiva. Además, está optimizada para un despliegue sencillo en la plataforma Render, eliminando la necesidad de usar la terminal.

## 2. Arquitectura del Sistema

El sistema se compone de una aplicación web construida con Flask (Python) en el backend y HTML, CSS, JavaScript en el frontend. Utiliza SendGrid para el envío de correos electrónicos y procesa enlaces de Google Drive para la entrega de contenido.

- **Backend (Flask)**:
    - `src/main.py`: Punto de entrada de la aplicación Flask, configura rutas y la base de datos.
    - `src/email_service.py`: Módulo encargado de la lógica de envío de correos electrónicos a través de SendGrid.
    - `src/link_generator.py`: Módulo que procesa y genera los enlaces de regalo, incluyendo la lógica específica para Google Drive.
    - `src/routes/gift.py`: Define las rutas API para el envío de correos de regalo.
    - `src/routes/link_generator_routes.py`: Define las rutas API para la generación de enlaces de regalo.
    - `src/config.py`: Archivo de configuración para la aplicación, incluyendo la clave API de SendGrid y la configuración de la base de datos.

- **Frontend (HTML/CSS/JavaScript)**:
    - `src/static/index.html`: La interfaz principal del dashboard, que incluye las secciones de "Generar Enlaces" y "Enviar Regalos".
    - `regalo.html`: La plantilla HTML que se envía a los destinatarios, mostrando el regalo y el nuevo modal de valoraciones.

- **Base de Datos (SQLite)**:
    - `instance/site.db`: Base de datos SQLite utilizada para almacenar información de los regalos generados (opcional, se puede expandir).

## 3. Prerrequisitos

Para ejecutar el proyecto localmente, necesitarás:

- Python 3.x
- `pip` (administrador de paquetes de Python)
- Una cuenta de SendGrid con una clave API y un remitente verificado.

## 4. Configuración Local

1.  **Clonar el repositorio (o extraer el archivo comprimido):**
    ```bash
    # Si es un repositorio
    git clone <URL_DEL_REPOSITORIO>
    cd rohayhu_dashboard
    # Si es un archivo comprimido
    tar -xzvf rohayhu_dashboard_integrado_final.tar.gz
    cd rohayhu_dashboard
    ```

2.  **Crear y activar un entorno virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # En Linux/macOS
    # venv\Scripts\activate  # En Windows
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar la clave API de SendGrid:**
    Abre `src/config.py` y reemplaza `YOUR_SENDGRID_API_KEY` con tu clave API de SendGrid. También asegúrate de que `SENDGRID_SENDER_EMAIL` sea tu remitente verificado.

    ```python
    # src/config.py
    SENDGRID_API_KEY = 'SG.YOUR_SENDGRID_API_KEY'
    SENDGRID_SENDER_EMAIL = 'tu_remitente_verificado@ejemplo.com'
    ```

5.  **Ejecutar la aplicación Flask:**
    ```bash
    python src/main.py
    ```

    La aplicación estará disponible en `http://127.0.0.1:5000`.

## 5. Uso del Dashboard

El dashboard tiene dos pestañas principales:

### 5.1. Generar Enlaces

1.  **Nombre del Receptor**: Ingresa el nombre de la persona que recibirá el regalo.
2.  **¿Es un Kit de Recuerdos?**: Marca esta opción si el regalo es un kit (permite múltiples componentes).
3.  **Componentes del Regalo**: Haz clic en "Añadir Video", "Añadir Audio", "Añadir PDF" o "Añadir Link" para agregar los componentes. Para Google Drive, pega el enlace para compartir. El sistema extraerá automáticamente el ID y generará la URL de visualización/descarga correcta.
4.  **Generar Enlace Mágico**: Haz clic para obtener el enlace personalizado.
5.  **Copiar Enlace**: Copia el enlace generado al portapapeles.
6.  **Usar para Enviar**: Copia automáticamente el nombre del receptor y el enlace generado a la pestaña "Enviar Regalos".

### 5.2. Enviar Regalos

1.  **Nombre del Destinatario**: Se puede autocompletar desde la pestaña "Generar Enlaces" o ingresarse manualmente.
2.  **Email del Destinatario**: Ingresa la dirección de correo electrónico del destinatario.
3.  **Nombre del Remitente**: Ingresa tu nombre o el de tu empresa.
4.  **URL del Regalo**: Se puede autocompletar desde la pestaña "Generar Enlaces" o ingresarse manualmente.
5.  **Enviar Regalo Mágico**: Haz clic para enviar el correo electrónico.

## 6. Despliegue en Render

Para desplegar la aplicación en Render, sigue estos pasos:

1.  **Sube tu proyecto a un repositorio de Git** (GitHub, GitLab, Bitbucket).
2.  **Crea una nueva Web Service en Render:**
    - Inicia sesión en Render y haz clic en "New Web Service".
    - Conecta tu repositorio de Git.
    - Configura los siguientes parámetros:
        - **Name**: `rohayhu-celebra-dashboard` (o el nombre que prefieras)
        - **Region**: Selecciona la región más cercana a tus usuarios.
        - **Branch**: `main` (o la rama principal de tu proyecto)
        - **Root Directory**: `/` (si tu `main.py` está en la raíz del repositorio)
        - **Runtime**: `Python 3`
        - **Build Command**: `pip install -r requirements.txt`
        - **Start Command**: `gunicorn src.main:app` (asegúrate de que `gunicorn` esté en `requirements.txt`)

3.  **Variables de Entorno (Environment Variables):**
    - Agrega `SENDGRID_API_KEY` con tu clave API de SendGrid.
    - Agrega `SENDGRID_SENDER_EMAIL` con tu dirección de correo electrónico de remitente verificada.

4.  **Despliegue:** Haz clic en "Create Web Service". Render construirá y desplegará automáticamente tu aplicación. Una vez desplegada, tendrás una URL pública para acceder a tu dashboard.

## 7. Mejoras Implementadas

Esta versión del dashboard incluye las siguientes mejoras significativas:

-   **Procesamiento Avanzado de Google Drive**: La lógica de generación de enlaces (`src/link_generator.py`) ahora detecta automáticamente el tipo de archivo de Google Drive (video, audio, PDF) y genera la URL de visualización/descarga correcta (`uc?export=view&id=` para videos/audios, `/preview` para PDFs).
-   **Mejoras de Diseño en `regalo.html`**:
    -   **Contraste Mejorado**: El contenedor principal de la página de regalo (`.gift-container`) ahora tiene un fondo sólido gris oscuro (`#393d41`) para un mejor contraste y legibilidad del texto blanco.
    -   **Texto Blanco Consistente**: Se aseguró que todo el texto dentro del contenedor principal sea blanco para mantener la coherencia y mejorar la visibilidad.
-   **Modal de Valoraciones Integrado**: Se ha añadido un modal de valoraciones en `regalo.html` que aparece cuando el usuario intenta cerrar la ventana o después de 30 segundos en la página. Este modal incluye enlaces directos para dejar reseñas en Google, Instagram y Facebook, con un diseño atractivo y botones con colores de marca.
    -   **Enlaces de Valoración**: Se han corregido los enlaces para Google, Instagram y Facebook para asegurar que dirijan a las páginas correctas de reseña/perfil.
-   **Dashboard Integrado**: Todas las funcionalidades (generación de enlaces y envío de correos) están ahora en un único dashboard web, con una navegación por pestañas intuitiva.
-   **Preparación para Despliegue en Render**: Se han incluido archivos de configuración (`render.yaml`, `.gitignore`) y se ha adaptado la aplicación para un despliegue sin problemas en Render, utilizando `gunicorn` para producción.

## 8. Solución de Problemas

-   **Error 403 de SendGrid**: Asegúrate de que tu clave API de SendGrid sea correcta y que la dirección de correo electrónico del remitente esté verificada en tu cuenta de SendGrid.
-   **Problemas de Despliegue en Render**: Revisa los logs de construcción y despliegue en el panel de control de Render. Asegúrate de que todas las dependencias estén en `requirements.txt` y que las variables de entorno estén configuradas correctamente.
-   **Enlaces de Google Drive no funcionan**: Verifica que los enlaces de Google Drive sean públicos y que la lógica en `src/link_generator.py` esté procesando correctamente los IDs.

---
