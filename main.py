from scheduler.system import System
from utilities.mqtt_broker import MQTTBroker

mqtt_broker = MQTTBroker()
watering = System(mqtt_broker, "local_db.json", "Preemptive")
watering.run_blocking()