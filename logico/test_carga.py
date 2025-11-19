"""
Pruebas de Carga para LogiCo
Ejecutar: locust -f test_carga.py --host=http://127.0.0.1:8000

Requisitos:
pip install locust
"""

from locust import HttpUser, task, between
import random
import json

class LogicoUser(HttpUser):
    """Usuario simulado para pruebas de carga"""
    wait_time = between(1, 3)  # Espera entre 1 y 3 segundos entre tareas
    
    def on_start(self):
        """Se ejecuta al inicio de cada usuario simulado"""
        # Login y obtener token
        response = self.client.post("/api/token/", json={
            "username": "admin",
            "password": "admin123"
        })
        if response.status_code == 200:
            self.token = response.json().get("token")
            self.headers = {"Authorization": f"Token {self.token}"}
        else:
            # Si falla, intentar con otro usuario
            response = self.client.post("/api/token/", json={
                "username": "coordinador1",
                "password": "coord123"
            })
            if response.status_code == 200:
                self.token = response.json().get("token")
                self.headers = {"Authorization": f"Token {self.token}"}
    
    @task(3)
    def ver_dashboard(self):
        """Ver dashboard - Tarea más frecuente"""
        self.client.get("/dashboard/", headers=self.headers)
    
    @task(2)
    def listar_ordenes(self):
        """Listar órdenes"""
        self.client.get("/ordenes/", headers=self.headers)
    
    @task(2)
    def listar_ordenes_api(self):
        """Listar órdenes vía API"""
        self.client.get("/api/ordenes/", headers=self.headers)
    
    @task(1)
    def listar_despachos(self):
        """Listar despachos"""
        self.client.get("/despachos/", headers=self.headers)
    
    @task(1)
    def listar_motos(self):
        """Listar motos"""
        self.client.get("/motos/", headers=self.headers)
    
    @task(1)
    def listar_usuarios(self):
        """Listar usuarios"""
        self.client.get("/usuarios/", headers=self.headers)
    
    @task(1)
    def crear_orden_api(self):
        """Crear orden vía API"""
        clientes = [
            "Cliente Test 1", "Cliente Test 2", "Cliente Test 3",
            "Cliente Test 4", "Cliente Test 5"
        ]
        direcciones = [
            "Av. Principal 123", "Calle Secundaria 456",
            "Boulevard Central 789", "Avenida Norte 321"
        ]
        
        self.client.post("/api/ordenes/", json={
            "cliente": random.choice(clientes),
            "direccion": random.choice(direcciones),
            "telefono_cliente": f"9{random.randint(10000000, 99999999)}",
            "descripcion": "Orden de prueba de carga",
            "tipo": random.choice(["normal", "receta_detendida"]),
            "prioridad": random.choice(["alta", "media", "baja"]),
            "estado_actual": "retiro_receta"
        }, headers=self.headers)
    
    @task(1)
    def obtener_detalle_orden(self):
        """Obtener detalle de orden aleatoria"""
        # Primero obtener lista de órdenes
        response = self.client.get("/api/ordenes/", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("results") and len(data["results"]) > 0:
                orden_id = random.choice(data["results"])["id"]
                self.client.get(f"/api/ordenes/{orden_id}/", headers=self.headers)
    
    @task(1)
    def filtrar_ordenes(self):
        """Filtrar órdenes por estado"""
        estados = ["retiro_receta", "traslado", "despacho", "re_despacho"]
        estado = random.choice(estados)
        self.client.get(f"/ordenes/?estado={estado}", headers=self.headers)
    
    @task(1)
    def buscar_ordenes(self):
        """Buscar órdenes"""
        terminos = ["test", "cliente", "medicamento", "urgente"]
        termino = random.choice(terminos)
        self.client.get(f"/ordenes/?search={termino}", headers=self.headers)


class LogicoAPILoadTest(HttpUser):
    """Pruebas de carga específicas para API REST"""
    wait_time = between(0.5, 2)
    
    def on_start(self):
        """Login y obtener token"""
        response = self.client.post("/api/token/", json={
            "username": "admin",
            "password": "admin123"
        })
        if response.status_code == 200:
            self.token = response.json().get("token")
            self.headers = {"Authorization": f"Token {self.token}"}
    
    @task(5)
    def listar_ordenes(self):
        """Listar órdenes - Operación más frecuente"""
        self.client.get("/api/ordenes/", headers=self.headers)
    
    @task(3)
    def listar_despachos(self):
        """Listar despachos"""
        self.client.get("/api/despachos/", headers=self.headers)
    
    @task(2)
    def listar_motos(self):
        """Listar motos"""
        self.client.get("/api/motos/", headers=self.headers)
    
    @task(2)
    def crear_orden(self):
        """Crear orden"""
        self.client.post("/api/ordenes/", json={
            "cliente": f"Cliente Carga {random.randint(1, 1000)}",
            "direccion": f"Dirección {random.randint(1, 1000)}",
            "telefono_cliente": f"9{random.randint(10000000, 99999999)}",
            "tipo": "normal",
            "prioridad": "media"
        }, headers=self.headers)
    
    @task(1)
    def obtener_detalle(self):
        """Obtener detalle de orden"""
        response = self.client.get("/api/ordenes/", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("results") and len(data["results"]) > 0:
                orden_id = random.choice(data["results"])["id"]
                self.client.get(f"/api/ordenes/{orden_id}/", headers=self.headers)

