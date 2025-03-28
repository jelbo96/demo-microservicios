from influxdb_client import InfluxDBClient
from datetime import datetime, timedelta

INFLUX_URL = "http://influx:8086"
INFLUX_TOKEN = "admintesttoken"
INFLUX_ORG = "pruebainfluxdb"
INFLUX_BUCKET = "system"

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
query_api = client.query_api()

def parse_time_search(timeSearch: str):
    """Convierte '15m', '3h', '2d' en un datetime en UTC."""
    try:
        num = int(timeSearch[:-1])
        unit = timeSearch[-1]
        if unit == "m":
            return datetime.utcnow() - timedelta(minutes=num)
        elif unit == "h":
            return datetime.utcnow() - timedelta(hours=num)
        elif unit == "d":
            return datetime.utcnow() - timedelta(days=num)
        else:
            return None
    except:
        return None

def fetch_data_from_influx(version: int, timeSearch: str):
    """Consulta InfluxDB y obtiene los datos filtrados."""
    start_time = parse_time_search(timeSearch)
    if start_time is None:
        return None, "Parámetro timeSearch inválido"

    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    query = f'''
        from(bucket: "{INFLUX_BUCKET}")
        |> range(start: time(v: "{start_time_str}"))
        |> filter(fn: (r) => r._measurement == "dispositivos")
        |> filter(fn: (r) => r.version == "{version}")
        |> keep(columns: ["_time", "_value", "version"])
    '''

    try:
        tables = query_api.query(org=INFLUX_ORG, query=query)
        return tables, None
    except Exception as e:
        return None, str(e)
