import json
import requests

# === CONFIGURAÇÕES DA API ===
DEVICE_ID = "4225410056"
API_URL = f"https://kunakcloud.com/openAPIv0/v1/rest/devices/{DEVICE_ID}/elements/insert"
API_USERNAME = "semad_adm"
API_PASSWORD = "Cimear@2025"

# === LER CONFIGURAÇÃO DO ARQUIVO ===
TRANSLATE_FILE = "translate.json"

# === FUNÇÃO PARA INSERIR ELEMENTO ===
def insert_element(element_data):
    """
    Cria e envia o JSON de inserção de um elemento baseado no arquivo translate.json
    """
    # Usa Translated_Element se existir, senão usa Element
    tag_name = element_data.get("Translated_Element", element_data["Element"])
    
    # Define decimal_places baseado no campo do JSON ou, se não existir, aplica heurística por unidade
    if "decimal_places" in element_data:
        decimal_places = element_data["decimal_places"]
    else:
        # heurística simples baseada em units
        units = element_data.get("Units", "")
        if units in ["ppb", "ppm"]:
            decimal_places = 2
        elif units in ["°C", "%", "hPa", "mm", "m/s", "dB", "ug/m3"]:
            decimal_places = 1
        elif units == "°":
            decimal_places = 0
        else:
            decimal_places = 2  # default

    payload = {
        "tag": tag_name,
        "unit": element_data.get("Units", ""),
        "type_id": 1,  # Tipo fixo, ajustar se necessário
        "manufacturer": "Kunak Technologies",
        "serial_number": f"AUTO_{element_data['Element']}",
        "model": "Default Model",
        "decimal_places": decimal_places,
        "sampling_period": 900,
        "start_time": "00:00:00",
        "end_time": "23:59:59",
        "max": "",
        "min": "",
        "persistence": 9,
        "x0": "0.0",
        "x1": "1.0",
        "x2": "0.0"
    }

    # === ENVIO DO POST ===
    try:
        response = requests.post(
            API_URL,
            auth=(API_USERNAME, API_PASSWORD),
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=10
        )

        if response.status_code == 200:
            print(f"Elemento criado: {payload['tag']} (decimal_places={decimal_places})")
        else:
            print(f"Erro ({response.status_code}) ao criar {payload['tag']}: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao criar {payload['tag']}: {e}")


# === EXECUÇÃO ===
def main():
    # Lê o arquivo translate.json
    with open(TRANSLATE_FILE, "r", encoding="utf-8") as f:
        translate_data = json.load(f)

    # Itera pelos elementos dentro de "Data"
    for element in translate_data["Data"]:
        insert_element(element)


if __name__ == "__main__":
    main()
