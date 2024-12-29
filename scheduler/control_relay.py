from utilities.rs485 import Fertilizer
from design_pattern.observer import Observer
import os

class ControlRelay(Observer):
  def __init__(self) -> None:
    super().__init__()
      
  def update(self, data):
    # fer = Fertilizer()
    feed_id = data[0]
    payload = data[1]

    # if (feed_id == f"{os.getenv('DEVICE_CODE')}/feeds/area1/pump1"):
    #   if payload == "1":
    #     fer.control_relay(1, True)
    #     # print("open 1")
    #   else:
    #     fer.control_relay(1, False)
    #     # print("close 1")
    # if (feed_id == f"{os.getenv('DEVICE_CODE')}/feeds/area1/pump2"):
    #   if payload == "1":
    #     # print("open 2")
    #     fer.control_relay(2, True)
    #   else:
    #     # print("close 2")
    #     fer.control_relay(2, False)