import json
import os
import sys
import pymongo

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

print("--- OPERACIONES CRUD EN MONGODB ---\n")

# 1. Conexion
print("1. Conectando a MongoDB...")
try:
    cliente = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
    cliente.server_info()
except Exception as error:
    print(f"Error: No se pudo conectar a MongoDB. Revisa que este encendido.\nDetalle: {error}")
    exit(1)

bd = cliente["DataSaludNoSQL"]
coleccion = bd["atenciones_clinicas"]
coleccion.drop()
print("Conectado a la base de datos 'DataSaludNoSQL'. Coleccion lista.\n")

# 2. CREATE
print("2. [CREATE] Insertando pacientes desde archivo JSON...")
ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_json = os.path.join(ruta_actual, "datos_atenciones_semiestructuradas.json")

with open(ruta_json, "r", encoding="utf-8") as archivo:
    datos_pacientes = json.load(archivo)

resultado = coleccion.insert_many(datos_pacientes)
print(f"Se guardaron {len(resultado.inserted_ids)} pacientes:")

for p in datos_pacientes:
    id_at = p.get("id_atencion")
    enf = p.get("enfermedad")
    edad = p.get("paciente", {}).get("edad")
    sexo = p.get("paciente", {}).get("sexo")
    lugar = p.get("distrito")
    print(f" - {id_at}: {enf} ({edad} anos, {sexo}, {lugar})")
print()

# 3. READ
print("3. [READ] Buscando pacientes que requieren hospitalizacion...")
filtro = {"datos_clinicos.requiere_hospitalizacion": True}
hospitalizados = list(coleccion.find(filtro))
print(f"Se encontraron {len(hospitalizados)} pacientes:")

for p in hospitalizados:
    id_at = p.get("id_atencion")
    enf = p.get("enfermedad")
    cama = p.get("datos_clinicos", {}).get("cama_asignada")
    plaquetas = p.get("datos_clinicos", {}).get("plaquetas", "-")
    signos = p.get("datos_clinicos", {}).get("signos_alarma", [])
    print(f" * {id_at} ({enf})")
    print(f"   Cama: {cama} | Plaquetas: {plaquetas} | Signos: {', '.join(signos)}")
print()

# 4. UPDATE
print("4. [UPDATE] Actualizando datos del paciente AT-2024-00101...")
p_antes = coleccion.find_one({"id_atencion": "AT-2024-00101"})
print(f" Antes -> Plaquetas: {p_antes['datos_clinicos']['plaquetas']} | Favorable: {p_antes['datos_clinicos']['evolucion_favorable']}")

coleccion.update_one(
    {"id_atencion": "AT-2024-00101"},
    {
        "$set": {
            "datos_clinicos.plaquetas": 135000,
            "datos_clinicos.evolucion_favorable": True,
            "datos_clinicos.observaciones_alta": "Paciente recuperada, dada de alta."
        }
    }
)

p_despues = coleccion.find_one({"id_atencion": "AT-2024-00101"})
print(f" Despues -> Plaquetas: {p_despues['datos_clinicos']['plaquetas']} | Favorable: {p_despues['datos_clinicos']['evolucion_favorable']}")
print(f" Nota: {p_despues['datos_clinicos']['observaciones_alta']}\n")

# 5. DELETE
print("5. [DELETE] Borrando al paciente AT-2024-00103 (caso leve)...")
coleccion.delete_one({"id_atencion": "AT-2024-00103"})
total = coleccion.count_documents({})
print(f"Paciente borrado. Quedan {total} pacientes en la coleccion:")
for p in coleccion.find():
    print(f" - {p['id_atencion']}: {p['enfermedad']}")

print("\nOperaciones CRUD completadas.")
