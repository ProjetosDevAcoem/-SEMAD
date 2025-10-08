import json

# Arquivo TXT contendo os dados
txt_file = "dados.txt"
# JSON de referência com Translated_Element
json_file = "translate.json"
# Arquivo de saída
output_file = "output.json"

# Lê o JSON de referência
with open(json_file, "r", encoding="utf-8") as f:
    dados_json = json.load(f)

# Lê o arquivo TXT e transforma em lista
with open(txt_file, "r", encoding="utf-8") as f:
    conteudo = f.read().strip()

# Divide os dados pelo separador ";"
valores = conteudo.split(";")

# Extrai informações fixas do TXT
station = valores[0]
date = valores[1]
time = valores[2]
timestamp = int(valores[3])

# Monta um dicionário de dados do TXT (nome -> valor)
txt_dict = {}
i = 4  # começa depois de station, date, time, timestamp
while i + 1 < len(valores):  # garante que i e i+1 existem
    chave = valores[i]
    valor = valores[i + 1]
    # tenta converter para float se possível
    try:
        valor = float(valor)
    except ValueError:
        pass
    txt_dict[chave] = valor
    i += 3  # pula a unidade


# Atualiza o JSON de referência
if "Data" in dados_json:
    for item in dados_json["Data"]:
        # Substitui Translated_Element por Element
        if "Translated_Element" in item:
            item["Element"] = item["Translated_Element"]
            del item["Translated_Element"]
        # Atualiza o Value se o nome existir no TXT
        key = item["Element"]
        if key in txt_dict:
            item["Value"] = txt_dict[key]

# Adiciona informações fixas
dados_json["Station"] = station
dados_json["Date"] = date
dados_json["Time"] = time
dados_json["Timestamp"] = timestamp

# Salva o JSON final
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(dados_json, f, indent=4, ensure_ascii=False)

print(f"JSON gerado com sucesso: {output_file}")
