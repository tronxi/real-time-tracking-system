import json, pika, datetime, random, time
from pika import credentials

def generate_event():
    pitch = round(random.uniform(-90, 90), 2)
    roll  = round(random.uniform(-180, 180), 2)
    yaw   = round(random.uniform(0, 360), 2)

    lat = round(random.uniform(40.0, 41.0), 6)
    lon = round(random.uniform(-3.8, -3.6), 6)
    return {
        "type": "TM",
        "datetime": datetime.datetime.now().isoformat(),
        "payload": {
            "altitude": round(random.uniform(0, 50), 2),
            "temperature": round(random.uniform(15, 30), 1),
            "lat": lat,
            "long": lon,
            "pitch": pitch,
            "roll": roll,
            "yaw": yaw,
        }
    }
conn = pika.BlockingConnection(pika.ConnectionParameters(
    host='tronxi.ddns.net',
    port=5672,
    credentials=credentials.PlainCredentials(
        username="rocket",
        password="rocket"
    ),
    heartbeat=60
))
ch = conn.channel()

print("Enviando eventos simulados... (Ctrl+C para detener)")
try:
    while True:
        evt = generate_event()
        ch.basic_publish(exchange="tracking_device_events",
                         routing_key="",
                         body=json.dumps(evt).encode())
        print("Evento publicado:", evt)
        time.sleep(2)
except KeyboardInterrupt:
    print("Simulación detenida.")
    conn.close()