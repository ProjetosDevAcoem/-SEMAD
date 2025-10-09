import json
import requests
from requests.auth import HTTPBasicAuth

# =========================
# CONFIGURAÇÕES
# =========================

API_USERNAME = "semad_adm"
API_PASSWORD = "Cimear@2025"
API_URL = "https://kunakcloud.com/openAPIv0/v1/rest/devices/{KUNAK_STATIONS}/elements/reads/insert"

TXT_FILE = "dados.txt"
TRANSLATE_FILE = "translate.json"


# =========================
# FUNÇÕES PRINCIPAIS
# =========================

def load_translate_map(translate_file):
    """Lê o arquivo translate.json e cria um dicionário Element → Translated_Element."""
    with open(translate_file, "r", encoding="utf-8") as f:
        translate_data = json.load(f)

    translate_dict = {}
    if "Data" in translate_data:
        for item in translate_data["Data"]:
            translate_dict[item["Element"]] = item["Translated_Element"]
    return translate_dict


def read_txt_data(txt_file):
    """Lê o arquivo TXT e extrai os valores em formato de dicionário."""
    with open(txt_file, "r", encoding="utf-8") as f:
        conteudo = f.read().strip()

    valores = conteudo.split(";")

    station = valores[0]
    date = valores[1]
    time = valores[2]
    timestamp = int(valores[3])

    data_dict = {"Station": station, "Date": date, "Time": time, "TimeStamp": timestamp}
    i = 4
    while i + 1 < len(valores):
        chave = valores[i]
        valor = valores[i + 1]
        try:
            valor = float(valor)
        except ValueError:
            valor = None
        data_dict[chave] = valor
        i += 3  # pula o nome, valor e unidade

    return data_dict


def format_data_for_api(txt_data, translate_dict):
    """Monta o corpo JSON no formato esperado pela API da Kunak."""
    timestamp = txt_data["TimeStamp"] * 1000  # Kunak usa milissegundos
    values = []

    for element, translated in translate_dict.items():
        if element in txt_data and txt_data[element] is not None:
            valor = txt_data[element]
            # Exemplo de ajuste de escala para CO, se necessário
            if element.startswith("CO_"):
                valor *= 1000

            values.append({
                "tag": translated,     # vem de translate.json
                "value": f"{valor:.3f}",
                "validation": "T",
                "reason": "0"
            })

    return [{
        "timestamp": str(timestamp),
        "values": values
    }]


def send_data_to_api(data):
    """Envia os dados formatados para a API Kunak."""
    if not data:
        print("Nenhum dado formatado para enviar.")
        return

    try:
        response = requests.post(API_URL, json=data, auth=HTTPBasicAuth(API_USERNAME, API_PASSWORD))
        if response.status_code == 200:
            print("Dados enviados com sucesso.")
        else:
            print(f"Erro ao enviar os dados: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")


def main():
    print("Lendo mapeamento de tradução...")
    translate_dict = load_translate_map(TRANSLATE_FILE)

    print("Lendo dados do arquivo TXT...")
    txt_data = read_txt_data(TXT_FILE)

    print("Formatando dados para envio...")
    data = format_data_for_api(txt_data, translate_dict)

    print("Enviando para a Kunak Cloud...")
    send_data_to_api(data)

    print("Processo concluído.")


# =========================
# EXECUÇÃO
# =========================
if __name__ == "__main__":
    main()
