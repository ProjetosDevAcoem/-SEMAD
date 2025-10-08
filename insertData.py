import json

# Arquivos
txt_file = "dados.txt"
json_file = "translate.json"
output_file = "output.json"

# 1️⃣ Lê o JSON de referência (apenas para metadados)
with open(json_file, "r", encoding="utf-8") as f:
    ref_json = json.load(f)

# Cria um dicionário para acessar Type e Description pelo Element do TXT
meta_dict = {}
if "Data" in ref_json:
    for item in ref_json["Data"]:
        key = item["Element"]  # pega o Element original que corresponde ao TXT
        meta_dict[key] = {
            "Type": item.get("Type", ""),
            "Description": item.get("Description", "")
        }

# 2️⃣ Lê o TXT
with open(txt_file, "r", encoding="utf-8") as f:
    conteudo = f.read().strip()

valores = conteudo.split(";")

# 3️⃣ Extrai informações fixas do TXT
station = valores[0]
date = valores[1]
time = valores[2]
timestamp = int(valores[3])

# 4️⃣ Monta lista de dados combinando TXT + metadados do JSON
data_list = []
i = 4  # começa depois de station, date, time, timestamp
while i + 1 < len(valores):
    chave = valores[i]                     # nome do elemento do TXT
    valor = valores[i + 1]                 # valor do TXT
    unidade = valores[i + 2] if i + 2 < len(valores) else ""

    # Converte para float se possível
    try:
        valor = float(valor)
    except ValueError:
        pass

    # Busca metadados do JSON de referência
    meta = meta_dict.get(chave, {})
    tipo = meta.get("Type", "")
    descricao = meta.get("Description", "")

    # Adiciona ao data_list
    data_list.append({
        "Element": chave,
        "Value": valor,
        "Units": unidade,
        "Type": tipo,
        "Description": descricao
    })

    i += 3  # pula para o próximo conjunto

# 5️⃣ Monta JSON final
json_final = {
    "Station": station,
    "Date": date,
    "Time": time,
    "Timestamp": timestamp,
    "Data": data_list
}

# 6️⃣ Salva JSON final
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(json_final, f, indent=4, ensure_ascii=False)

print(f"JSON gerado com sucesso: {output_file}")
