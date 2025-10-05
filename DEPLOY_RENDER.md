# Despliegue en Render - Rohayhu Celebra! Dashboard

## Pasos para Desplegar en Render

### 1. Preparar el Repositorio

1. **Subir el código a GitHub**:
   - Crear un nuevo repositorio en GitHub
   - Subir todos los archivos del proyecto
   - Asegurar que `render.yaml` esté en la raíz del proyecto

### 2. Configurar en Render

1. **Crear cuenta en Render**: [https://render.com](https://render.com)

2. **Conectar con GitHub**:
   - Ir a Dashboard → "New" → "Web Service"
   - Conectar tu cuenta de GitHub
   - Seleccionar el repositorio del proyecto

3. **Configuración automática**:
   - Render detectará automáticamente el archivo `render.yaml`
   - La configuración se aplicará automáticamente

### 3. Variables de Entorno (Opcional)

Si quieres cambiar la clave de SendGrid:

1. En el dashboard de Render, ir a "Environment"
2. Agregar/modificar:
   - `SENDGRID_API_KEY`: Tu clave API de SendGrid
   - `FLASK_ENV`: `production`

### 4. Despliegue

1. **Despliegue automático**: Render iniciará el despliegue automáticamente
2. **Tiempo estimado**: 3-5 minutos
3. **URL**: Render proporcionará una URL pública (ej: `https://rohayhu-celebra-dashboard.onrender.com`)

## Configuración Actual

### Archivo `render.yaml`
```yaml
services:
  - type: web
    name: rohayhu-celebra-dashboard
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python src/main.py
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: SENDGRID_API_KEY
        value: [CLAVE_ACTUAL_CONFIGURADA]
      - key: FLASK_ENV
        value: production
    healthCheckPath: /api/health
```

### Características del Plan Gratuito de Render

- ✅ **Gratis**: Sin costo
- ✅ **HTTPS automático**: Certificado SSL incluido
- ✅ **Dominio personalizado**: Posible agregar tu propio dominio
- ⚠️ **Hibernación**: Se duerme después de 15 minutos de inactividad
- ⚠️ **Tiempo de arranque**: 30-60 segundos al despertar
- ✅ **750 horas/mes**: Suficiente para uso normal

## Verificación Post-Despliegue

### 1. Verificar Estado del Sistema
- Acceder a tu URL de Render
- Hacer clic en "🔍 Verificar Estado del Sistema"
- Debe mostrar "✅ Sistema funcionando correctamente"

### 2. Probar Generación de Enlaces
- Ir a la pestaña "🔗 Generar Enlaces"
- Crear un enlace de prueba
- Verificar que se genere correctamente

### 3. Probar Envío de Correos
- Ir a la pestaña "📧 Enviar Regalos"
- Enviar un correo de prueba a tu email
- Verificar que llegue correctamente

## Solución de Problemas

### Error de Despliegue
- Revisar los logs en el dashboard de Render
- Verificar que `requirements.txt` esté actualizado
- Confirmar que la estructura de archivos sea correcta

### Error de SendGrid
- Verificar que la clave API sea válida
- Confirmar que el remitente esté verificado
- Revisar los límites de la cuenta gratuita

### Aplicación No Responde
- Verificar que la aplicación no esté hibernando
- Hacer una solicitud para "despertar" el servicio
- Revisar los logs de errores en Render

## Mantenimiento

### Actualizaciones
- Hacer push al repositorio de GitHub
- Render desplegará automáticamente los cambios

### Monitoreo
- Usar el dashboard de Render para ver métricas
- Revisar logs de errores regularmente
- Monitorear el uso de SendGrid

## URLs Importantes

- **Dashboard de Render**: [https://dashboard.render.com](https://dashboard.render.com)
- **SendGrid Dashboard**: [https://app.sendgrid.com](https://app.sendgrid.com)
- **Documentación de Render**: [https://render.com/docs](https://render.com/docs)

---

¡Tu dashboard estará disponible 24/7 en internet sin necesidad de mantener tu computadora encendida! 🚀
