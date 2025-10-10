import json
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
from glob import glob
import os

# === CONFIGURAÇÕES DA API ===
API_USERNAME = "semad_adm"
API_PASSWORD = "Cimear@2025"
API_BASE_URL = "https://kunakcloud.com/openAPIv0/v1/rest/devices/{device_id}/elements/reads/insert"

# === CONFIGURAÇÕES DE PASTA E LOG ===
TXT_FOLDER = "./"
TRANSLATE_FILE = "translate.json"
LOG_FILE = "erro_api.log"

# === MAPEAMENTO DE ARQUIVOS PARA DEVICE IDs ===
DEVICE_MAP = {
    "ECQ008-22_": "4225410056",
}

# === LÊ O ARQUIVO DE TRADUÇÃO ===
def translate_tags(translate_file):
    with open(translate_file, "r", encoding="utf-8") as f:
        translate_data = json.load(f)

    translate_dict = {}
    if "Data" in translate_data:
        for item in translate_data["Data"]:
            translated_name = item.get("Translated_Element", item["Element"])
            translate_dict[item["Element"]] = translated_name
    return translate_dict

# === LÊ OS DADOS DE UM ARQUIVO .TXT ===
def read_txt_data(txt_file):
    with open(txt_file, "r", encoding="utf-8") as f:
        conteudo = f.read().strip()

    valores = conteudo.split(";")
    if len(valores) < 5:
        raise ValueError(f"Arquivo {txt_file} mal formatado ou incompleto.")

    station = valores[0]
    date = valores[1]
    time = valores[2]
    timestamp = float(valores[3])

    data_dict = {"Station": station, "Date": date, "Time": time, "Timestamp": timestamp}
    i = 4
    while i + 2 < len(valores):
        chave = valores[i]
        valor = valores[i + 1]
        try:
            valor = float(valor)
        except ValueError:
            valor = 0.0  # Substitui valores ausentes por zero
        data_dict[chave] = valor
        i += 3  # nome, valor e unidade
    return data_dict

# === FORMATA PARA JSON KUNAK ===
def format_data_for_api(txt_data, translate_dict):
    timestamp = int(txt_data["Timestamp"] * 1000)
    values = []

    for element, translated_name in translate_dict.items():
        if element in txt_data:
            valor = txt_data[element]
            valor_str = str(valor)  # Sempre envia como string
            values.append({
                "tag": translated_name,
                "value": valor_str,
                "validation": "T",
                "reason": "0"
            })

    if not values:
        raise ValueError("Nenhum valor válido encontrado para envio.")

    payload = [{
        "timestamp": str(timestamp),
        "values": values
    }]

    return payload

# === ENVIA OS DADOS PARA A API ===
def send_data_to_api(device_id, data):
    api_url = API_BASE_URL.format(device_id=device_id)
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(
            api_url,
            headers=headers,
            auth=HTTPBasicAuth(API_USERNAME, API_PASSWORD),
            data=json.dumps(data)
        )

        if response.status_code == 200:
            print(f"[{datetime.now()}] Dados enviados com sucesso para device {device_id}.")
        else:
            print(f"[{datetime.now()}] Erro HTTP {response.status_code} no envio para device {device_id}.")
            print(response.text)
            with open(LOG_FILE, "a", encoding="utf-8") as log_file:
                log_file.write(f"{datetime.now()} - Erro {response.status_code} ({device_id}): {response.text}\n")

    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now()}] Erro na requisição para device {device_id}: {e}")
        with open(LOG_FILE, "a", encoding="utf-8") as log_file:
            log_file.write(f"{datetime.now()} - Exceção ({device_id}): {e}\n")

# === PROCESSA TODOS OS ARQUIVOS ===
def process_files():
    print(f"[{datetime.now()}] Iniciando processamento de arquivos...\n")
    translate_dict = translate_tags(TRANSLATE_FILE)

    for pattern, device_id in DEVICE_MAP.items():
        file_pattern = os.path.join(TXT_FOLDER, f"{pattern}*")
        txt_files = glob(file_pattern)

        if not txt_files:
            print(f"Nenhum arquivo encontrado para o prefixo {pattern}")
            continue

        for txt_file in txt_files:
            try:
                print(f"Lendo arquivo: {os.path.basename(txt_file)}")
                txt_data = read_txt_data(txt_file)
                payload = format_data_for_api(txt_data, translate_dict)

                # Mostra o JSON final antes de enviar
                print(json.dumps(payload, indent=4, ensure_ascii=False))

                print(f"Enviando dados para o device {device_id}...")
                send_data_to_api(device_id, payload)

            except Exception as e:
                print(f"[{datetime.now()}] Erro ao processar {txt_file}: {e}")
                with open(LOG_FILE, "a", encoding="utf-8") as log_file:
                    log_file.write(f"{datetime.now()} - Erro ao processar {txt_file}: {e}\n")

    print(f"\n[{datetime.now()}] Processamento concluído.")

if __name__ == "__main__":
    process_files()
