# Dashboard Rohayhu Celebra! 🎁

Una aplicación web moderna para automatizar el envío de regalos digitales personalizados.

## Inicio Rápido

### 1. Activar el entorno virtual
```bash
source venv/bin/activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación
```bash
python src/main.py
```

### 4. Acceder al dashboard
Abrir en el navegador: `http://127.0.0.1:5000`

## Uso

1. **Verificar estado del sistema** - Se hace automáticamente al cargar la página
2. **Completar el formulario** con los datos del regalo:
   - Nombre del destinatario
   - Email del destinatario  
   - Nombre del remitente
   - URL del regalo (generada por generador.html)
3. **Hacer clic en "Enviar Regalo Mágico"**
4. **Confirmar el envío exitoso**

## Características

- ✨ Interfaz web moderna y responsive
- 🎨 Diseño con colores corporativos de Rohayhu Celebra!
- 📧 Integración completa con SendGrid
- 🔍 Verificación automática del estado del sistema
- 💌 Plantillas HTML personalizadas para correos
- 🎯 Validación de formularios en tiempo real
- 🎉 Retroalimentación visual de éxito/error

## Estructura del Proyecto

```
rohayhu_dashboard/
├── src/
│   ├── main.py              # Aplicación Flask principal
│   ├── email_service.py     # Servicio de envío de correos
│   ├── routes/gift.py       # API endpoints
│   └── static/index.html    # Dashboard web
├── plantilla_email.html     # Plantilla de correo
├── requirements.txt         # Dependencias
└── README.md               # Este archivo
```

## Configuración de SendGrid

La aplicación está configurada para usar SendGrid con la cuenta verificada `rohayhuregaleria@gmail.com`. 

Para cambiar la configuración, editar `src/email_service.py` y asegurar que:
- La clave API tenga permisos de envío
- El remitente esté verificado en SendGrid

## Solución de Problemas

### Error 403 de SendGrid
- Verificar que la clave API sea válida
- Confirmar que el remitente esté verificado

### Error de conexión
- Verificar que el servidor Flask esté ejecutándose
- Comprobar que el puerto 5000 esté disponible

### Formulario no responde
- Habilitar JavaScript en el navegador
- Completar todos los campos obligatorios

## Documentación Completa

Ver `DOCUMENTACION_DASHBOARD.md` para información detallada sobre arquitectura, API, seguridad y mantenimiento.

---

**Desarrollado por Manus AI para Rohayhu Celebra!** 🚀
