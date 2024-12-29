from typing import Callable, Any
from paho.mqtt.client import Client, MQTTMessage
from design_pattern.observer import Subject
from dotenv import load_dotenv
from time import sleep
import os
import sys

class MQTTBroker(Subject):
    def __init__(self):
        super().__init__()
        if load_dotenv():
            self._FEED_IDS = [
                ("relay1", 1), ("relay2", 1), ("relay3", 1), ("relay4", 1),
                ("relay5", 1), ("relay6", 1), ("relay7", 1), ("relay8", 1), ("schedules", 2),
                ("area1/pump1", 2), ("area1/pump2", 2)
            ]
            self.subscription_map = {}  # To map mid to topic and QoS

            self._MQTT_BROKER_USERNAME = os.getenv("MQTT_BROKER_USERNAME")
            self._MQTT_BROKER_PASSWORD = os.getenv("MQTT_BROKER_PASSWORD")
            self._DEVICE_CODE = os.getenv("DEVICE_CODE")
            self._MQTT_BROKER_URL = os.getenv("MQTT_BROKER_URL")
            self._MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT"))  # Default port 1883
        else:
            print("Fail to read from env")
            sys.exit(1)

        self._client = Client(client_id=self._MQTT_BROKER_USERNAME)
        self._client.username_pw_set(self._MQTT_BROKER_USERNAME, self._MQTT_BROKER_PASSWORD)

        # Callbacks
        self._client.on_connect = self._connected
        self._client.on_disconnect = self._disconnected
        self.set_on_message(self._default_on_message)
        self._client.on_subscribe = self._subscribed

        # Enable auto-reconnect
        self._client.reconnect_delay_set(min_delay=1, max_delay=120)

        # Connect to the broker
        try:
            self._client.connect(self._MQTT_BROKER_URL, self._MQTT_BROKER_PORT, keepalive=60)
            self._client.loop_start()  # Run the loop in the background
        except Exception as e:
            print(f"Failed to connect to the broker: {e}")
            sys.exit(1)

    def _connected(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully ...")
            # Subscribe to topics with specified QoS
            for topic, qos in self._FEED_IDS:
                full_topic = f"{self._DEVICE_CODE}/feeds/{topic}"
                try:
                    result, mid = self._client.subscribe(full_topic, qos)
                    self.subscription_map[mid] = (full_topic, qos)  # Map mid to topic and QoS
                except Exception as e:
                    print(f"Failed to subscribe to {full_topic}: {e}")
        else:
            print(f"Connection failed with code {rc}")
            sys.exit(1)

    def _disconnected(self, client, userdata, rc):
        print("Disconnected ... Attempting to reconnect.")
        while True:
            try:
                self._client.reconnect()
                print("Reconnected successfully.")
                break
            except Exception as e:
                print(f"Reconnection failed: {e}. Retrying in 5 seconds...")
                sleep(5)

    def _subscribed(self, client, userdata, mid, granted_qos):
        topic, qos = self.subscription_map.get(mid, ("Unknown", "Unknown"))
        print(f"Subscription confirmed: Topic={topic}, Requested QoS={qos}, Granted QoS={granted_qos[0]}")

    def _default_on_message(self, client, userdata, msg):
        print(f"Received message: {msg.payload.decode()}, topic: {msg.topic}")
        # Send notification to observers
        self.send_notify([msg.topic, msg.payload.decode()])

    def publish(self, feed_id, value, qos):
        topic = f"{self._DEVICE_CODE}/feeds/{feed_id}"
        try:
            self._client.publish(topic, value, qos)
            print(f"Published {value} to {topic}")
        except Exception as e:
            print(f"Failed to publish message: {e}")

    def set_on_message(self, callback: Callable[[Client, Any, MQTTMessage], None]):
        self._client.on_message = callback
