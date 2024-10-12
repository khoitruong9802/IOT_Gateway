import serial.tools.list_ports
import time

class PortNotFound(Exception):
    def __init__(self, message="Port cannot be found"):
        self.message = message
        super().__init__(self.message)

class Serial:
    def __init__(self):
        self.ser = serial.Serial( port=self.get_port(), baudrate=115200)
        self._mess = ""

    def get_port(self):
        ports = serial.tools.list_ports.comports()
        if ports:
            return ports[0].device
        else:
            raise PortNotFound()
        
    def send_data(self, data):
        self.ser.write(data.encode())

    def process_data(self, data):
        data = data.replace("!", "")
        data = data.replace("#", "")
        splitData = data.split(":")
        return splitData

    def run(self, callback=None):
        while True:
            bytesToRead = self.ser.inWaiting()
            if (bytesToRead > 0):
                self._mess = self._mess + self.ser.read(bytesToRead).decode("UTF-8")
                while ("#" in self._mess) and ("!" in self._mess):
                    start = self._mess.find("!")
                    end = self._mess.find("#")
                    if callback is not None:
                        callback(self.process_data(self._mess[start:end + 1]))
                    if (end == len(self._mess)):
                        self._mess = ""
                    else:
                        self._mess = self._mess[end+1:]
            time.sleep(1)

if __name__ == "__main__":
    ser = Serial()
    # ser.run()