from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)  # Permitir peticiones desde el frontend Next.js

# Datos simulados en memoria (en producción usarías una base de datos)
dashboard_stats = {
    "llamadas_totales": 1234,
    "llamadas_activas": 23,
    "llamadas_perdidas": 45,
    "tiempo_promedio": "4:32"
}

clientes = [
    {
        "id": 1,
        "nombre": "Juan Pérez",
        "email": "juan@email.com",
        "telefono": "+34 600 123 456",
        "ciudad": "Madrid",
        "llamadas": 12,
        "ultima_llamada": "2024-01-15"
    },
    {
        "id": 2,
        "nombre": "Ana Martínez",
        "email": "ana@email.com",
        "telefono": "+34 600 234 567",
        "ciudad": "Barcelona",
        "llamadas": 8,
        "ultima_llamada": "2024-01-14"
    },
    {
        "id": 3,
        "nombre": "Pedro Gómez",
        "email": "pedro@email.com",
        "telefono": "+34 600 345 678",
        "ciudad": "Valencia",
        "llamadas": 15,
        "ultima_llamada": "2024-01-16"
    },
    {
        "id": 4,
        "nombre": "Sofía Torres",
        "email": "sofia@email.com",
        "telefono": "+34 600 456 789",
        "ciudad": "Sevilla",
        "llamadas": 6,
        "ultima_llamada": "2024-01-13"
    },
    {
        "id": 5,
        "nombre": "Miguel Ruiz",
        "email": "miguel@email.com",
        "telefono": "+34 600 567 890",
        "ciudad": "Bilbao",
        "llamadas": 20,
        "ultima_llamada": "2024-01-16"
    }
]

llamadas = [
    {
        "id": 1,
        "cliente": "Juan Pérez",
        "agente": "María García",
        "tipo": "Entrante",
        "duracion": "5:23",
        "estado": "Completada",
        "fecha": "2024-01-16 10:30"
    },
    {
        "id": 2,
        "cliente": "Ana Martínez",
        "agente": "Carlos López",
        "tipo": "Saliente",
        "duracion": "3:45",
        "estado": "En curso",
        "fecha": "2024-01-16 11:15"
    },
    {
        "id": 3,
        "cliente": "Pedro Gómez",
        "agente": "Laura Sánchez",
        "tipo": "Entrante",
        "duracion": "0:00",
        "estado": "Perdida",
        "fecha": "2024-01-16 09:45"
    }
]

agentes = [
    {
        "id": 1,
        "nombre": "María García",
        "email": "maria@callcenter.com",
        "estado": "Disponible",
        "llamadas_hoy": 12,
        "rating": 4.8,
        "extension": "101"
    },
    {
        "id": 2,
        "nombre": "Carlos López",
        "email": "carlos@callcenter.com",
        "estado": "En llamada",
        "llamadas_hoy": 8,
        "rating": 4.6,
        "extension": "102"
    },
    {
        "id": 3,
        "nombre": "Laura Sánchez",
        "email": "laura@callcenter.com",
        "estado": "Disponible",
        "llamadas_hoy": 15,
        "rating": 4.9,
        "extension": "103"
    },
    {
        "id": 4,
        "nombre": "Roberto Díaz",
        "email": "roberto@callcenter.com",
        "estado": "Descanso",
        "llamadas_hoy": 10,
        "rating": 4.7,
        "extension": "104"
    }
]

# ============ ENDPOINTS DE DASHBOARD ============

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Obtener estadísticas del dashboard"""
    return jsonify(dashboard_stats)

@app.route('/api/dashboard/actividad-reciente', methods=['GET'])
def get_actividad_reciente():
    """Obtener actividad reciente del call center"""
    actividades = [
        {
            "agente": "María García",
            "accion": "Llamada completada",
            "cliente": "Juan Pérez",
            "tiempo": "Hace 2 min",
            "estado": "success"
        },
        {
            "agente": "Carlos López",
            "accion": "Llamada en curso",
            "cliente": "Ana Martínez",
            "tiempo": "5:23",
            "estado": "active"
        },
        {
            "agente": "Laura Sánchez",
            "accion": "Llamada perdida",
            "cliente": "Pedro Gómez",
            "tiempo": "Hace 8 min",
            "estado": "missed"
        }
    ]
    return jsonify(actividades)

# ============ ENDPOINTS DE CLIENTES ============

@app.route('/api/clientes', methods=['GET'])
def get_clientes():
    """Obtener lista de clientes"""
    search = request.args.get('search', '')
    estado = request.args.get('estado', 'todos')  # todos, activos, inactivos
    
    resultado = clientes
    
    if search:
        resultado = [c for c in resultado if 
                    search.lower() in c['nombre'].lower() or 
                    search.lower() in c['email'].lower() or 
                    search.lower() in c['telefono'].lower()]
    
    return jsonify(resultado)

@app.route('/api/clientes/<int:cliente_id>', methods=['GET'])
def get_cliente(cliente_id):
    """Obtener un cliente específico"""
    cliente = next((c for c in clientes if c['id'] == cliente_id), None)
    if cliente:
        return jsonify(cliente)
    return jsonify({"error": "Cliente no encontrado"}), 404

@app.route('/api/clientes', methods=['POST'])
def crear_cliente():
    """Crear un nuevo cliente"""
    data = request.json
    nuevo_cliente = {
        "id": max([c['id'] for c in clientes]) + 1,
        "nombre": data.get('nombre'),
        "email": data.get('email'),
        "telefono": data.get('telefono'),
        "ciudad": data.get('ciudad'),
        "llamadas": 0,
        "ultima_llamada": None
    }
    clientes.append(nuevo_cliente)
    return jsonify(nuevo_cliente), 201

@app.route('/api/clientes/<int:cliente_id>', methods=['PUT'])
def actualizar_cliente(cliente_id):
    """Actualizar un cliente existente"""
    cliente = next((c for c in clientes if c['id'] == cliente_id), None)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404
    
    data = request.json
    cliente.update({
        "nombre": data.get('nombre', cliente['nombre']),
        "email": data.get('email', cliente['email']),
        "telefono": data.get('telefono', cliente['telefono']),
        "ciudad": data.get('ciudad', cliente['ciudad'])
    })
    return jsonify(cliente)

@app.route('/api/clientes/<int:cliente_id>', methods=['DELETE'])
def eliminar_cliente(cliente_id):
    """Eliminar un cliente"""
    global clientes
    clientes = [c for c in clientes if c['id'] != cliente_id]
    return jsonify({"mensaje": "Cliente eliminado"}), 200

# ============ ENDPOINTS DE LLAMADAS ============

@app.route('/api/llamadas', methods=['GET'])
def get_llamadas():
    """Obtener lista de llamadas"""
    estado = request.args.get('estado', 'todas')  # todas, activas, completadas, perdidas
    
    resultado = llamadas
    
    if estado != 'todas':
        resultado = [l for l in resultado if l['estado'].lower() == estado.lower()]
    
    return jsonify(resultado)

@app.route('/api/llamadas/<int:llamada_id>', methods=['GET'])
def get_llamada(llamada_id):
    """Obtener una llamada específica"""
    llamada = next((l for l in llamadas if l['id'] == llamada_id), None)
    if llamada:
        return jsonify(llamada)
    return jsonify({"error": "Llamada no encontrada"}), 404

@app.route('/api/llamadas', methods=['POST'])
def crear_llamada():
    """Registrar una nueva llamada"""
    data = request.json
    nueva_llamada = {
        "id": max([l['id'] for l in llamadas]) + 1,
        "cliente": data.get('cliente'),
        "agente": data.get('agente'),
        "tipo": data.get('tipo'),
        "duracion": "0:00",
        "estado": "En curso",
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    llamadas.append(nueva_llamada)
    return jsonify(nueva_llamada), 201

@app.route('/api/llamadas/<int:llamada_id>', methods=['PUT'])
def actualizar_llamada(llamada_id):
    """Actualizar una llamada existente"""
    llamada = next((l for l in llamadas if l['id'] == llamada_id), None)
    if not llamada:
        return jsonify({"error": "Llamada no encontrada"}), 404
    
    data = request.json
    llamada.update({
        "duracion": data.get('duracion', llamada['duracion']),
        "estado": data.get('estado', llamada['estado'])
    })
    return jsonify(llamada)

# ============ ENDPOINTS DE AGENTES ============

@app.route('/api/agentes', methods=['GET'])
def get_agentes():
    """Obtener lista de agentes"""
    estado = request.args.get('estado', 'todos')  # todos, disponible, ocupado, descanso
    
    resultado = agentes
    
    if estado != 'todos':
        resultado = [a for a in resultado if a['estado'].lower() == estado.lower()]
    
    return jsonify(resultado)

@app.route('/api/agentes/<int:agente_id>', methods=['GET'])
def get_agente(agente_id):
    """Obtener un agente específico"""
    agente = next((a for a in agentes if a['id'] == agente_id), None)
    if agente:
        return jsonify(agente)
    return jsonify({"error": "Agente no encontrado"}), 404

@app.route('/api/agentes/<int:agente_id>/estado', methods=['PUT'])
def actualizar_estado_agente(agente_id):
    """Actualizar el estado de un agente"""
    agente = next((a for a in agentes if a['id'] == agente_id), None)
    if not agente:
        return jsonify({"error": "Agente no encontrado"}), 404
    
    data = request.json
    agente['estado'] = data.get('estado', agente['estado'])
    return jsonify(agente)

# ============ ENDPOINTS DE REPORTES ============

@app.route('/api/reportes/rendimiento', methods=['GET'])
def get_reporte_rendimiento():
    """Obtener reporte de rendimiento"""
    periodo = request.args.get('periodo', 'hoy')  # hoy, semana, mes
    
    reporte = {
        "periodo": periodo,
        "total_llamadas": random.randint(100, 500),
        "llamadas_completadas": random.randint(80, 400),
        "llamadas_perdidas": random.randint(10, 50),
        "tiempo_promedio": f"{random.randint(3, 8)}:{random.randint(10, 59)}",
        "satisfaccion_cliente": round(random.uniform(4.0, 5.0), 1)
    }
    return jsonify(reporte)

@app.route('/api/reportes/agentes', methods=['GET'])
def get_reporte_agentes():
    """Obtener reporte de rendimiento de agentes"""
    return jsonify([
        {
            "agente": a['nombre'],
            "llamadas": a['llamadas_hoy'],
            "rating": a['rating'],
            "tiempo_promedio": f"{random.randint(3, 8)}:{random.randint(10, 59)}"
        }
        for a in agentes
    ])

# ============ ENDPOINT DE SALUD ============

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificar que el servidor está funcionando"""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Servidor Flask iniciando en http://localhost:5000")
    print("📡 API disponible en http://localhost:5000/api")
    app.run(debug=True, port=5000)
