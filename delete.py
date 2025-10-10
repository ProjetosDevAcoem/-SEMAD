import requests

API_USERNAME = "semad_adm"
API_PASSWORD = "Cimear@2025"
DEVICE_ID = "4225410056"

ELEMENTS = [
    # "AirTemp_Avg",
    # "IntTemp_Avg",
    # "NO2_Avg",
    # "Noise_Max",
    # "O3_Avg",
    # "PM2.5_Avg",
    # "PM10_Avg",
    # "PressAtm_Avg",
    # "Rain_Total",
    # "RelUmid_Avg",
    # "SO2_Avg",
    # "VOC_Avg",
    # "WindDirection_ResAvg",
    # "WindSpeed_Avg",
    # "CO_Avg"
]

# ELEMENTS = [
#     "CO GCc AVG1H (ppb)",
#     "CO GCc AVG8H (ppb)",
#     "CO GCc AVG24H (ppb)",
#     "CO_Avg (ppm)",
#     "LAeq AVG1H (dB(A))",
#     "NO2 GCc AVG1H (ppb)",
#     "NO2 GCc AVG24H (ppb)",
#     "O3 GCc AVG1H (ppb)",
#     "O3 GCc AVG8H (ppb)",
#     "PM2.5 AVG1H (ug/m3)",
#     "PM2.5 AVG24H (ug/m3)",
#     "PM10 AVG1H (ug/m3)",
#     "PM10 AVG24H (ug/m3)",
#     "Rainfall 1H (mm)",
#     "SO2 GCc AVG1H (ppb)",
#     "SO2 GCc AVG24H (ppb)",
#     "VOCs GCc AVG1H (ppm)"
# ]


# ELEMENTS = [
#     "IntTemp",
#     "O3 GCc",
#     "CO GCc",
#     "NO2 GCc",
#     "SO2 GCc",
#     "VOCs GCc",
#     "PM2.5",
#     "PM10",
#     "LAeq",
#     "Temp ext",
#     "Humidity ext",
#     "Pressure",
#     "Rainfall",
#     "W Speed AVG",
#     "W Vane AVG"
# ]

for element in ELEMENTS:
    api_url = f"https://kunakcloud.com/openAPIv0/v1/rest/devices/{DEVICE_ID}/elements/{element}/delete"
    try:
        response = requests.get(api_url, auth=(API_USERNAME, API_PASSWORD))
        if response.status_code == 200:
            print(f"✅ Elemento {element} apagado com sucesso.")
        else:
            print(f"❌ Erro ({response.status_code}) ao apagar {element}: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Erro de conexão ao apagar {element}: {e}")
