import requests
import pprint

def test_api(objetivo, calorias=None):
    url = "http://localhost:5000/recomendar"
    payload = {"objetivo": objetivo}
    if calorias:
        payload["calorias"] = calorias
    
    response = requests.post(url, json=payload)
    pprint.pprint(response.json())

print("--PRUEBEA PARA BAJAR DE PESO--")
test_api("bajar")

print("\n -- PRUEBA DE 2600 CALORIAS--")
test_api("calorias", 2600)