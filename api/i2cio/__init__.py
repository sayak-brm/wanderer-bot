#! /usr/bin/python3
import smbus2


class I2CError(OSError):
    pass


class I2CIO:
    def __init__(self, addr, bus_no=1):
        self.bus_no = bus_no
        self.bus = smbus2.SMBus(self.bus_no)
        self.addr = addr
        self.buffer = []

    def add_write(self, data):
        self.buffer.append(("w", smbus2.i2c_msg.write(self.addr, data)))

    def add_read(self, len):
        self.buffer.append(("r", smbus2.i2c_msg.read(self.addr, len)))

    def broadcast(self, attempt=1, max_attempts=3):
        try:
            self.bus.i2c_rdwr(*[msg[1] for msg in self.buffer])
        except OSError:
            print("#> Bus Error... Restarting bus.")
            print("#> Attempt: ", attempt, "/", max_attempts, sep="")
            self.bus = smbus2.SMBus(self.bus_no)
            if attempt >= max_attempts:
                raise I2CError
            self.broadcast(attempt + 1, max_attempts)

    def get_reads(self):
        reads = []
        for msg in self.buffer:
            if msg[0] == "r":
                reads += list(msg[1])
        self.buffer = []
        return reads

    def send_read(self, len):
        self.add_read(len)
        self.broadcast()
        return self.get_reads()

    def send_write(self, data):
        self.add_write(data)
        self.broadcast()
        self.buffer = []
