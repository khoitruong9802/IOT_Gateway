import paho.mqtt.client as mqtt
import time
import random

# MQTT broker details
BROKER = "34.143.214.138"  # Replace with your broker address
PORT = 1883  # Default MQTT port
TOPICS = [
    "18faa0dd7a927906cb3e/feeds/area1/temp",
    "18faa0dd7a927906cb3e/feeds/area1/humi",
    "18faa0dd7a927906cb3e/feeds/area1/kali",
    "18faa0dd7a927906cb3e/feeds/area1/nito",
    "18faa0dd7a927906cb3e/feeds/area1/photpho",
    "18faa0dd7a927906cb3e/feeds/area2/temp",
    "18faa0dd7a927906cb3e/feeds/area2/humi",
    "18faa0dd7a927906cb3e/feeds/area2/kali",
    "18faa0dd7a927906cb3e/feeds/area2/nito",
    "18faa0dd7a927906cb3e/feeds/area2/photpho",
    "18faa0dd7a927906cb3e/feeds/area3/temp",
    "18faa0dd7a927906cb3e/feeds/area3/humi",
    "18faa0dd7a927906cb3e/feeds/area3/kali",
    "18faa0dd7a927906cb3e/feeds/area3/nito",
    "18faa0dd7a927906cb3e/feeds/area3/photpho",
]

# Initialize previous values to simulate gradual changes
previous_values = {
    "temp": 25.0,  # Initial temperature in °C
    "humi": 60.0,  # Initial humidity in %
    "kali": 2.0,   # Initial potassium concentration in mg/kg
    "nito": 1.5,   # Initial nitrogen concentration in mg/kg
    "photpho": 1.0 # Initial phosphorus concentration in mg/kg
}

# Generate mock sensor data with realistic behavior
def generate_mock_data(topic):
    global previous_values

    if "temp" in topic:
        # Simulate gradual temperature changes with occasional spikes
        change = random.uniform(-0.5, 0.5)  # Small gradual change
        previous_values["temp"] += change
        if random.random() < 0.1:  # 10% chance of a spike
            previous_values["temp"] += random.uniform(-2, 2)
        return round(max(15.0, min(40.0, previous_values["temp"])), 1)  # Clamp between 15°C and 40°C

    elif "humi" in topic:
        # Simulate humidity with slow changes and random noise
        change = random.uniform(-1, 1)  # Gradual humidity change
        previous_values["humi"] += change
        if random.random() < 0.05:  # 5% chance of sudden change
            previous_values["humi"] += random.uniform(-10, 10)
        return round(max(20.0, min(100.0, previous_values["humi"])), 1)  # Clamp between 20% and 100%

    elif "kali" in topic:
        # Potassium concentration with random fluctuation
        change = random.uniform(-0.1, 0.1)
        previous_values["kali"] += change
        return round(max(0.1, min(10.0, previous_values["kali"])), 1)  # Clamp between 0.1 and 10 mg/kg

    elif "nito" in topic:
        # Nitrogen concentration with gradual changes
        change = random.uniform(-0.1, 0.2)
        previous_values["nito"] += change
        return round(max(0.1, min(8.0, previous_values["nito"])), 1)  # Clamp between 0.1 and 8 mg/kg

    elif "photpho" in topic:
        # Phosphorus concentration with steady changes
        change = random.uniform(-0.05, 0.1)
        previous_values["photpho"] += change
        return round(max(0.1, min(5.0, previous_values["photpho"])), 1)  # Clamp between 0.1 and 5 mg/kg

    return None

# Callback for successful connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

# Initialize MQTT client
client = mqtt.Client()
client.username_pw_set("kksfarm", "123456")
client.on_connect = on_connect

# Connect to broker
try:
    client.connect(BROKER, PORT, keepalive=60)
except Exception as e:
    print(f"Could not connect to broker: {e}")
    exit(1)

# Publish mock data to topics periodically
try:
    while True:
        for topic in TOPICS:
            data = generate_mock_data(topic)
            client.publish(topic, data, retain=True, qos=0)
            print(f"Published {data} to {topic}")

        # client.publish("18faa0dd7a927906cb3e/feeds/notification", "thong bao", qos=0)
        time.sleep(60)  # Delay between each batch of publications
except KeyboardInterrupt:
    print("Stopping publisher...")

# Disconnect from broker
client.disconnect()
