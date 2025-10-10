import json
from datetime import datetime
from glob import glob
import os

# === CONFIGURAÇÕES DE PASTA ===
TXT_FOLDER = "./"
TRANSLATE_FILE = "translate.json"

# === LÊ O ARQUIVO DE TRADUÇÃO ===
def translate_tags(translate_file):
    with open(translate_file, "r", encoding="utf-8") as f:
        translate_data = json.load(f)

    translate_dict = {}
    if "Data" in translate_data:
        for item in translate_data["Data"]:
            translated_name = item.get("Translated_Element", item["Element"])
            translate_dict[item["Element"]] = {
                "Translated_Element": translated_name,
                "decimal_places": item.get("decimal_places", 2)
            }
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
            valor = None
        data_dict[chave] = valor
        i += 3  # nome, valor e unidade
    return data_dict

# === FORMATA PARA JSON KUNAK ===
def format_data_for_api(txt_data, translate_dict):
    timestamp = int(txt_data["Timestamp"] * 1000)  # converte para milissegundos
    values = []

    for element, info in translate_dict.items():
        if element in txt_data:
            valor = txt_data[element]
            dp = info["decimal_places"]

            if valor is None:
                valor_out = None
            else:
                # Formata como string com as casas decimais
                valor_out = f"{round(valor, dp):.{dp}f}"

            values.append({
                "tag": info["Translated_Element"],
                "value": valor_out,
                "validation": "T",
                "reason": "0"
            })

    payload = [{
        "timestamp": str(timestamp),
        "values": values
    }]

    return payload

# === PROCESSA UM ARQUIVO E EXIBE JSON ===
def process_and_print():
    translate_dict = translate_tags(TRANSLATE_FILE)

    # Exemplo: pega o primeiro arquivo encontrado
    txt_files = glob(os.path.join(TXT_FOLDER, "ECQ008-22_*"))
    if not txt_files:
        print("Nenhum arquivo encontrado.")
        return

    txt_data = read_txt_data(txt_files[0])
    payload = format_data_for_api(txt_data, translate_dict)

    # Exibe JSON formatado
    print(json.dumps(payload, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    process_and_print()
