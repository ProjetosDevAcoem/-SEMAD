import requests
import mysql.connector
import datetime
from requests.auth import HTTPBasicAuth

# Configuração da API
API_USERNAME = "portoalegre_adm"
API_PASSWORD = "IZSz6bZrvm?z"
API_URL = "https://kunakcloud.com/openAPIv0/v1/rest/devices/4225140015/elements/reads/insert"

# Configuração do banco de dados MySQL
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'wwacoe_kunak_projetos',
    'password': 'QwwM|MsHaqo(',
    'database': 'wwacoe_kunak_estacoes',
}

# Mapeamento das colunas do banco para as tags da API
COLUMN_TO_TAG = {
    "co": "CO GCc",
    "no": "NO GCc",
    "co2": "CO2 GCc",
    "no2": "NO2 GCc",
    "nox": "NOx GCc",
    "so2": "SO2 GCc",
    "o3": "O3 GCc",
    "pm10": "PM10",
    "pm25": "PM2.5",
    "temp": "Temp ext",
    "umid": "Humidity ext",
    "press": "Pressure",
    "vel": "W Speed AVG",
    "dir": "W Vane AVG",
    "rad": "Solar rad",
    "chuva": "Rainfall"
}


def fetch_latest_data():
    """ Obtém as últimas x linhas da tabela emqarmovel. """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM emqarmovel ORDER BY TimeStamp DESC LIMIT 1"
        cursor.execute(query)
        rows = cursor.fetchall()
        
        return rows
    except mysql.connector.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def format_data_for_api(rows):
    """ Formata as últimas 400 linhas de dados para o formato esperado pela API da Kunak Cloud. """
    if not rows:
        return None
    
    data = []
    for row in rows:
        timestamp = int(row["TimeStamp"]) * 1000  # Mantém o timestamp original com milissegundos
        values = []
        
        for col, tag in COLUMN_TO_TAG.items():
            if col in row and row[col] is not None:
                value = row[col] * 1000 if col == "co" else row[col]  # Multiplica CO por 1000
                values.append({
                    "tag": tag,
                    "value": f"{value:.3f}",
                    "validation": "T",
                    "reason": "0"
                })
        
        if values:
            data.append({
                "timestamp": str(timestamp),
                "values": values
            })
    
    return data if data else None


def send_data_to_api(data):
    """ Envia os dados formatados para a API da Kunak Cloud. """
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
    """ Executa o fluxo completo: busca os últimos 400 dados, formata e envia para a API. """
    print("Buscando últimas 400 linhas do banco...")
    rows = fetch_latest_data()
    
    print("Formatando dados...")
    data = format_data_for_api(rows)
    
    print("Enviando dados para a API...")
    send_data_to_api(data)
    
    print("Processo concluído.")


if __name__ == "__main__":
    main()