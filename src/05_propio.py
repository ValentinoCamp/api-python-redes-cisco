# Módulos que se usarán
import requests
from tabulate import tabulate

# URL base del Packet Tracer
baseUri = "http://localhost:58000/api/v1" 

# Headers
headers = {"Content-Type": "application/json"}
# Credenciales del Network Controller
data = {
    "username": "cisco",
    "password": "class"
}

# 1. Autenticación

resp = requests.post(baseUri + "/ticket", json=data, headers=headers)

if resp.status_code not in [200, 201]:
    print("Error al obtener el Service Ticket:", resp.status_code)
    print(resp.text)
    exit()

result = resp.json()
ticket = result["response"]["serviceTicket"]

print("\nAutenticación exitosa.")
print("\nService Ticket obtenido correctamente: ", ticket)

# 2. Consultar Discovery

headers = {"X-Auth-Token": ticket}
resp = requests.get(baseUri + "/discovery", headers=headers)

if resp.status_code != 200:
    print("Error al consultar Discovery:", resp.status_code)
    exit()

discoveries = resp.json().get("response", [])

# 3. Mostrar información
print("\n========== NETWORK DISCOVERY ==========\n")

discovery_list = []

for item in discoveries:
    discovery_list.append([
        item["name"],
        item["discoveryType"],
        item["discoveryStatus"],
        item["discoveryCondition"],
        item["ipAddressList"].replace(",", "\n")
    ])

print(tabulate(
    discovery_list,
    headers=["Nombre", "Tipo", "Estado", "Condición", "Direcciones IP"],
    tablefmt="rounded_grid"
))

# 4. Mostrar resumen
active = sum(1 for d in discoveries if d["discoveryStatus"] == "Active")
inactive = sum(1 for d in discoveries if d["discoveryStatus"] == "Inactive")
cdp = sum(1 for d in discoveries if d["discoveryType"] == "CDP")
iplist = sum(1 for d in discoveries if d["discoveryType"] == "IpList")

print("\n========== RESUMEN ==========")

summary = [
    ["Total de descubrimientos", len(discoveries)],
    ["Activos", active],
    ["Inactivos", inactive],
    ["Tipo CDP", cdp],
    ["Tipo IP List", iplist]
]

print(tabulate(
    summary,
    headers=["Categoría", "Cantidad"],
    tablefmt="rounded_grid"
))
