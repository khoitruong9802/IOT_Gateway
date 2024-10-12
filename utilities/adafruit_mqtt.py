from Adafruit_IO import MQTTClient
from design_pattern.observer import Subject
from dotenv import load_dotenv
import sys
import os

class AdafruitMQTT(Subject):
  def __init__(self):
    super().__init__()
    if load_dotenv():
      self.AIO_FEED_IDS = ["relay1", "relay2", "relay3", "relay4", "relay5", "relay6", "relay7", "relay8", "schedules"]
      self.AIO_USERNAME = os.getenv("AIO_USERNAME")
      self.AIO_KEY = os.getenv("AIO_KEY")
    else:
      print("Fail to read from env")
      sys.exit(1)

    self.client = MQTTClient(self.AIO_USERNAME , self.AIO_KEY)
    self.client.on_connect = self._connected
    self.client.on_disconnect = self._disconnected
    self.set_on_message(self._default_on_message)
    self.client.on_subscribe = self._subscribe
    self.client.connect()
    self.client.loop_background()
    # self.client.loop_blocking()

  def _connected(self, client):
    print("Ket noi thanh cong ...")
    for topic in self.AIO_FEED_IDS:
        self.client.subscribe(topic)

  def _subscribe(self, client, userdata, mid, granted_qos):
    print("Subscribe thanh cong ...")

  def _disconnected(self, client):
    print("Ngat ket noi ...")
    sys.exit(1)

  def _default_on_message(self, client, feed_id, payload):
    print("Nhan du lieu: " + payload + ", feed id: " + feed_id)
    self.send_notify([feed_id, payload])

  def publish(self, feed_id, value, group_id = None, feed_user = None):
    self.client.publish(feed_id, value, group_id, feed_user)

  def set_on_message(self, callback):
    self.client.on_message = callback
