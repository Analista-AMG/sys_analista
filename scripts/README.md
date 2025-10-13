# Backend Python Flask - Call Center

Este es el backend en Python con Flask para la aplicación de call center.

## Instalación

1. Instalar las dependencias:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Ejecutar el servidor

\`\`\`bash
python app.py
\`\`\`

El servidor se iniciará en `http://localhost:5000`

## Endpoints disponibles

### Dashboard
- `GET /api/dashboard/stats` - Estadísticas del dashboard
- `GET /api/dashboard/actividad-reciente` - Actividad reciente

### Clientes
- `GET /api/clientes` - Listar clientes
- `GET /api/clientes/<id>` - Obtener cliente específico
- `POST /api/clientes` - Crear nuevo cliente
- `PUT /api/clientes/<id>` - Actualizar cliente
- `DELETE /api/clientes/<id>` - Eliminar cliente

### Llamadas
- `GET /api/llamadas` - Listar llamadas
- `GET /api/llamadas/<id>` - Obtener llamada específica
- `POST /api/llamadas` - Registrar nueva llamada
- `PUT /api/llamadas/<id>` - Actualizar llamada

### Agentes
- `GET /api/agentes` - Listar agentes
- `GET /api/agentes/<id>` - Obtener agente específico
- `PUT /api/agentes/<id>/estado` - Actualizar estado del agente

### Reportes
- `GET /api/reportes/rendimiento` - Reporte de rendimiento
- `GET /api/reportes/agentes` - Reporte de agentes

### Salud
- `GET /api/health` - Verificar estado del servidor

## Notas

- El servidor usa datos en memoria (no persistentes)
- Para producción, deberías conectar una base de datos real
- CORS está habilitado para permitir peticiones desde el frontend Next.js
