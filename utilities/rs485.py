import time
import serial.tools.list_ports

class PortNotFound(Exception):
	def __init__(self, message="Port cannot be found"):
		self.message = message
		super().__init__(self.message)

class Fertilizer:
	def __init__(self, baudrate = 9600):
		self.port = self.get_port()
		self.baudrate = baudrate
		self.relay_commands = {
			"0_on": "01 05 00 00 FF 00 8C 3A",
			"0_off": "01 05 00 00 00 00 CD CA",
			"1_on": "01 05 00 01 FF 00 DD FA",
			"1_off": "01 05 00 01 00 00 9C 0A",
			"2_on": "01 05 00 02 FF 00 2D FA",
			"2_off": "01 05 00 02 00 00 6C 0A",
			"3_on": "01 05 00 03 FF 00 7C 3A",
			"3_off": "01 05 00 03 00 00 3D CA",
			"4_on": "01 05 00 04 FF 00 CD FB",
			"4_off": "01 05 00 04 00 00 8C 0B",
			"5_on": "01 05 00 05 FF 00 9C 3B",
			"5_off": "01 05 00 05 00 00 DD CB",
			"6_on": "01 05 00 06 FF 00 6C 3B",
			"6_off": "01 05 00 06 00 00 2D CB",
			"7_on": "01 05 00 07 FF 00 3D FB",
			"7_off": "01 05 00 07 00 00 7C 0B",
			"8_on": "01 05 00 08 FF 00 0D F8",
			"8_off": "01 05 00 08 00 00 4C 08",
		}
  
	def get_port(self):
		ports = serial.tools.list_ports.comports()
		if ports:
			return ports[0].device
		else:
			raise PortNotFound()

	def control_relay(self, relay_id: int, relay_state: bool):
		try:
			# Open the serial port
			with serial.Serial(self.port, self.baudrate, timeout=1) as ser:
				# Send the command
				command = self.relay_commands[f"{relay_id}_{'on' if relay_state else 'off'}"]
				ser.write(bytes.fromhex(command))
				print(f"Command {command} sent to the relay.")
				time.sleep(0.5)  # Give some time for the relay to process the command
		except Exception as e:
			print(f"Error: {e}")   

	def close_relay(relay_id: int):
		pass

	def run(self):
		return 0
		serial_port = "COM3"  # Update this to your actual RS485 port
		baudrate = 9600  # Update this to match your relay"s baudrate

		# Example to turn relay 0 on
		self.control_relay(serial_port, baudrate, self.relay_commands["relay_0_on"])
		time.sleep(1)

		# Example to turn relay 0 off
		self.control_relay(serial_port, baudrate, self.relay_commands["relay_0_off"])

