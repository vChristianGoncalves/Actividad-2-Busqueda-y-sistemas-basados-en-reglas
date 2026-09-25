from kanren import Relation, facts, run, var

# 1. BASE DE CONOCIMIENTO
# Calle 100 - Plaza Central
conecta = Relation()

facts(
    conecta,
    # Línea 1 (Roja)
    ("Portal Norte", "Calle 100", "Línea 1", 12),
    ("Calle 100", "Héroes", "Línea 1", 8),
    ("Héroes", "Calle 26", "Línea 1", 10),
    ("Calle 26", "Plaza Central", "Línea 1", 6),
    
    # Línea 2 (Azul)
    ("Suba", "Calle 100", "Línea 2", 15),
    ("Calle 100", "Parque Central", "Línea 2", 14),
    ("Parque Central", "Estación Sur", "Línea 2", 11),
    
    # Ofrece rutas alternativas
    ("Calle 100", "Calle 26", "Línea 3 Expresa", 15), 
    ("Aeropuerto", "Calle 26", "Línea 3", 18),
    ("Calle 26", "Estación Sur", "Línea 3", 16),
    ("Estacion Sur", "Plaza Central", "Línea 3", 9)    
)


# 2. MOTOR DE INFERENCIA
class MotorTransporteInteligente:
    def __init__(self, relacion_conexiones):
        self.relacion = relacion_conexiones

    def obtener_conexiones_directas(self, origen):
        destino_var = var()
        linea_var = var()
        tiempo_var = var()
        
        resultados = run(
            0, 
            (destino_var, linea_var, tiempo_var), 
            self.relacion(origen, destino_var, linea_var, tiempo_var)
        )
        return resultados

    def obtener_todas_las_rutas(self, origen, destino, visitados=None, camino_actual=None, tiempo_acumulado=0):
        if visitados is None:
            visitados = set()
        if camino_actual is None:
            camino_actual = []

        visitados.add(origen)
        todas_las_rutas = []

        # Caso base: Llegamos al destino objetivo
        if origen == destino:
            todas_las_rutas.append({
                "pasos": list(camino_actual),
                "tiempo_total": tiempo_acumulado
            })
        else:
            # Explorar todas las ramificaciones lógicas
            vecinos = self.obtener_conexiones_directas(origen)
            for prox_estacion, linea, tiempo in vecinos:
                if prox_estacion not in visitados:
                    nuevo_tramo = {
                        "origen": origen,
                        "destino": prox_estacion,
                        "linea": linea,
                        "tiempo": tiempo
                    }
                    camino_actual.append(nuevo_tramo)
                    
                    # Llamada recursiva explorando la nueva rama
                    rutas_encontradas = self.obtener_todas_las_rutas(
                        prox_estacion, 
                        destino, 
                        visitados.copy(), 
                        camino_actual, 
                        tiempo_acumulado + tiempo
                    )
                    todas_las_rutas.extend(rutas_encontradas)
                    
                    
                    camino_actual.pop()

        return todas_las_rutas


# 3. EJECUCIÓN
if __name__ == "__main__":
    sistema = MotorTransporteInteligente(conecta)

    origen_test = "Calle 100"
    destino_test = "Plaza Central"

    print(f"\nBuscando TODAS las rutas posibles desde '{origen_test}' hasta '{destino_test}'...\n")
    rutas = sistema.obtener_todas_las_rutas(origen_test, destino_test)

    if rutas:
        print(f"Se encontraron {len(rutas)} ruta(s) alternativa(s):\n")
        
        # Ordenamos opcionalmente por tiempo para mostrarlas organizadas
        rutas_ordenadas = sorted(rutas, key=lambda r: r['tiempo_total'])

        for idx, r in enumerate(rutas_ordenadas, 1):
            print(f"--- Opción {idx} (Tiempo total: {r['tiempo_total']} min) ---")
            for paso in r['pasos']:
                print(f"  • De [{paso['origen']}] a [{paso['destino']}] via {paso['linea']} ({paso['tiempo']} min)")
            print()
    else:
        print("No se encontraron rutas válidas entre los puntos especificados.")