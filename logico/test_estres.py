"""
Pruebas de Estrés para LogiCo
Ejecutar: locust -f test_estres.py --host=http://127.0.0.1:8000 --users=100 --spawn-rate=10

Requisitos:
pip install locust
"""

from locust import HttpUser, task, between, events
import random
import json
import time

class LogicoStressTest(HttpUser):
    """Pruebas de estrés - Muchos usuarios simultáneos"""
    wait_time = between(0.1, 0.5)  # Menos tiempo de espera para más carga
    
    def on_start(self):
        """Login rápido"""
        usuarios = [
            {"username": "admin", "password": "admin123"},
            {"username": "coordinador1", "password": "coord123"},
            {"username": "repartidor1", "password": "rep123"},
        ]
        creds = random.choice(usuarios)
        response = self.client.post("/api/token/", json=creds)
        if response.status_code == 200:
            self.token = response.json().get("token")
            self.headers = {"Authorization": f"Token {self.token}"}
        else:
            self.token = None
            self.headers = {}
    
    @task(10)
    def carga_intensiva_dashboard(self):
        """Carga intensiva en dashboard"""
        self.client.get("/dashboard/", headers=self.headers)
    
    @task(8)
    def carga_intensiva_ordenes(self):
        """Carga intensiva en listado de órdenes"""
        self.client.get("/ordenes/", headers=self.headers)
        # También hacer petición API
        self.client.get("/api/ordenes/", headers=self.headers)
    
    @task(5)
    def crear_multiples_ordenes(self):
        """Crear múltiples órdenes rápidamente"""
        for i in range(3):  # Crear 3 órdenes en secuencia
            self.client.post("/api/ordenes/", json={
                "cliente": f"Cliente Estrés {random.randint(1, 10000)}",
                "direccion": f"Dirección {random.randint(1, 10000)}",
                "telefono_cliente": f"9{random.randint(10000000, 99999999)}",
                "tipo": random.choice(["normal", "receta_detendida"]),
                "prioridad": random.choice(["alta", "media", "baja"])
            }, headers=self.headers)
    
    @task(5)
    def consultas_complejas(self):
        """Consultas complejas con filtros"""
        estados = ["retiro_receta", "traslado", "despacho", "re_despacho"]
        prioridades = ["alta", "media", "baja"]
        
        # Múltiples filtros simultáneos
        self.client.get(f"/ordenes/?estado={random.choice(estados)}&prioridad={random.choice(prioridades)}", 
                       headers=self.headers)
    
    @task(3)
    def operaciones_escritura_intensivas(self):
        """Operaciones de escritura intensivas"""
        # Crear orden
        orden_response = self.client.post("/api/ordenes/", json={
            "cliente": f"Cliente Estrés {time.time()}",
            "direccion": f"Dirección {random.randint(1, 10000)}",
            "telefono_cliente": f"9{random.randint(10000000, 99999999)}",
            "tipo": "normal",
            "prioridad": "media"
        }, headers=self.headers)
        
        # Si se creó, intentar actualizar
        if orden_response.status_code == 201:
            orden_id = orden_response.json().get("id")
            self.client.patch(f"/api/ordenes/{orden_id}/", json={
                "descripcion": "Actualización de prueba de estrés"
            }, headers=self.headers)
    
    @task(2)
    def acceso_concurrente_detalle(self):
        """Acceso concurrente a detalles"""
        # Obtener lista
        response = self.client.get("/api/ordenes/", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("results") and len(data["results"]) > 0:
                # Acceder a múltiples detalles
                for orden in random.sample(data["results"], min(3, len(data["results"]))):
                    self.client.get(f"/api/ordenes/{orden['id']}/", headers=self.headers)


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Se ejecuta al inicio de las pruebas de estrés"""
    print("=" * 60)
    print("INICIANDO PRUEBAS DE ESTRÉS")
    print("=" * 60)
    print(f"Host: {environment.host}")
    print(f"Usuarios objetivo: {environment.runner.target_user_count if hasattr(environment.runner, 'target_user_count') else 'N/A'}")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Se ejecuta al final de las pruebas de estrés"""
    print("=" * 60)
    print("FINALIZANDO PRUEBAS DE ESTRÉS")
    print("=" * 60)
    
    stats = environment.stats
    print(f"\nTotal de requests: {stats.total.num_requests}")
    print(f"Total de failures: {stats.total.num_failures}")
    print(f"Tasa de fallos: {(stats.total.num_failures / stats.total.num_requests * 100) if stats.total.num_requests > 0 else 0:.2f}%")
    print(f"Tiempo promedio de respuesta: {stats.total.avg_response_time:.2f}ms")
    print(f"Tiempo mínimo: {stats.total.min_response_time:.2f}ms")
    print(f"Tiempo máximo: {stats.total.max_response_time:.2f}ms")

