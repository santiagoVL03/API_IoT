import random
import time
import requests

BASE_URL = "http://localhost:8000/api/v1/iotgiroscopio/"

def generate_random_data():
    """Genera valores aleatorios simulando datos de giroscopio."""
    def maybe_none():
        return None if random.random() < 0.1 else round(random.uniform(-5.0, 5.0), 2)

    return {
        "ax": maybe_none(),
        "ay": maybe_none(),
        "az": maybe_none(),
        "gx": maybe_none(),
        "gy": maybe_none(),
        "gz": maybe_none()
    }

def fill_db_using_endpoint(endpoint, data):
    """Envía un GET con parámetros de query al endpoint del giroscopio."""
    params = {k: v for k, v in data.items() if v is not None}
    try:
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            print(f"Datos insertados: {data}")
        else:
            print(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"No se pudo conectar al endpoint: {e}")

def main():
    while True:
        data = generate_random_data()
        fill_db_using_endpoint(BASE_URL, data)
        time.sleep(random.uniform(0.5, 1))

if __name__ == "__main__":
    main()
