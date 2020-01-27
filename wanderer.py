#! /usr/bin/python3

from flask import Flask
from flask_restful import Resource, Api
from i2cio import I2CIO

app = Flask(__name__)
api = Api(app)
i2c = I2CIO(0x01)
app.config["DEBUG"] = True
motor_pins = {
    "ENAX": 13,
    "IN2X": 12,
    "IN1X": 11,
    "IN3X": 10,
    "IN4X": 9,
    "ENBX": 8,
    "ENAY": 3,
    "IN1Y": 14,
    "IN2Y": 15,
    "IN3Y": 16,
    "IN4Y": 17,
    "ENBY": 2
}
relay_pins = {
    "DRL": 37,
    "DIP": 39
}

class Initialize(Resource):
    @staticmethod
    def motor_init():
        for key in motor_pins.keys():
            i2c.send_write([1, motor_pins[key], 1])
            if key[:2] == "EN":
                i2c.send_write([4, motor_pins[key], 255])
            else:
                i2c.send_write([2, motor_pins[key], 0])
    
    @staticmethod
    def relay_init():
        for key in relay_pins.keys():
            i2c.send_write([1, relay_pins[key], 1])
            i2c.send_write([2, relay_pins[key], 1])
    
    def post(self):
        Initialize.motor_init()
        Initialize.relay_init()
        return {"success": True}

class Drive(Resource):
    @staticmethod
    def front():
        i2c.send_write([2, motor_pins["IN1X"], 0])
        i2c.send_write([2, motor_pins["IN2X"], 1])
        i2c.send_write([2, motor_pins["IN3X"], 1])
        i2c.send_write([2, motor_pins["IN4X"], 0])
        i2c.send_write([2, motor_pins["IN1Y"], 0])
        i2c.send_write([2, motor_pins["IN2Y"], 1])
        i2c.send_write([2, motor_pins["IN3Y"], 1])
        i2c.send_write([2, motor_pins["IN4Y"], 0])
        print("INF: Drive Front")

    @staticmethod
    def back():
        i2c.send_write([2, motor_pins["IN1X"], 1])
        i2c.send_write([2, motor_pins["IN2X"], 0])
        i2c.send_write([2, motor_pins["IN3X"], 0])
        i2c.send_write([2, motor_pins["IN4X"], 1])
        i2c.send_write([2, motor_pins["IN1Y"], 1])
        i2c.send_write([2, motor_pins["IN2Y"], 0])
        i2c.send_write([2, motor_pins["IN3Y"], 0])
        i2c.send_write([2, motor_pins["IN4Y"], 1])
        print("INF: Drive Back")

    @staticmethod
    def left():
        i2c.send_write([2, motor_pins["IN1X"], 0])
        i2c.send_write([2, motor_pins["IN2X"], 1])
        i2c.send_write([2, motor_pins["IN3X"], 0])
        i2c.send_write([2, motor_pins["IN4X"], 0])
        i2c.send_write([2, motor_pins["IN1Y"], 0])
        i2c.send_write([2, motor_pins["IN2Y"], 1])
        i2c.send_write([2, motor_pins["IN3Y"], 0])
        i2c.send_write([2, motor_pins["IN4Y"], 0])
        print("INF: Drive Left")

    @staticmethod
    def right():
        i2c.send_write([2, motor_pins["IN1X"], 0])
        i2c.send_write([2, motor_pins["IN2X"], 0])
        i2c.send_write([2, motor_pins["IN3X"], 1])
        i2c.send_write([2, motor_pins["IN4X"], 0])
        i2c.send_write([2, motor_pins["IN1Y"], 0])
        i2c.send_write([2, motor_pins["IN2Y"], 0])
        i2c.send_write([2, motor_pins["IN3Y"], 1])
        i2c.send_write([2, motor_pins["IN4Y"], 0])
        print("INF: Drive Right")

    @staticmethod
    def stop():
        i2c.send_write([2, motor_pins["IN1X"], 0])
        i2c.send_write([2, motor_pins["IN2X"], 0])
        i2c.send_write([2, motor_pins["IN3X"], 0])
        i2c.send_write([2, motor_pins["IN4X"], 0])
        i2c.send_write([2, motor_pins["IN1Y"], 0])
        i2c.send_write([2, motor_pins["IN2Y"], 0])
        i2c.send_write([2, motor_pins["IN3Y"], 0])
        i2c.send_write([2, motor_pins["IN4Y"], 0])
        print("INF: Drive Stop")

    def post(self, direction):
        if direction == "front":
            Drive.front()
        elif direction == "back":
            Drive.back()
        elif direction == "left":
            Drive.left()
        elif direction == "right":
            Drive.right()
        elif direction == "stop":
            Drive.stop()
        else:
            print("ERR: Incorrect Drive Direction")
            return {"success": False}
        return {"success": True}

class Sonar(Resource):
    def get(self):
        i2c.send_write([0])
        print("Sonar Requested")
        return i2c.send_read(3)

class Lights(Resource):
    @staticmethod
    def drl(state):
        if state=="on":
            i2c.send_write([2, relay_pins["DRL"], 0])
        if state=="off":
            i2c.send_write([2, relay_pins["DRL"], 1])
    
    @staticmethod
    def dip(state):
        if state=="on":
            i2c.send_write([2, relay_pins["DIP"], 0])
        if state=="off":
            i2c.send_write([2, relay_pins["DIP"], 1])
    
    def post(self, light, state):
        if light=="drl":
            Lights.drl(state)
        if light=="dip":
            Lights.dip(state)

class Gear(Resource):
    def post(self, number):
        if number == '1':
            i2c.send_write([4, motor_pins["ENAX"],  63])
            i2c.send_write([4, motor_pins["ENBX"],  63])
            i2c.send_write([4, motor_pins["ENAY"],  63])
            i2c.send_write([4, motor_pins["ENBY"],  63])
        elif number == '2':
            i2c.send_write([4, motor_pins["ENAX"], 127])
            i2c.send_write([4, motor_pins["ENBX"], 127])
            i2c.send_write([4, motor_pins["ENAY"], 127])
            i2c.send_write([4, motor_pins["ENBY"], 127])
        elif number == '3':
            i2c.send_write([4, motor_pins["ENAX"], 191])
            i2c.send_write([4, motor_pins["ENBX"], 191])
            i2c.send_write([4, motor_pins["ENAY"], 191])
            i2c.send_write([4, motor_pins["ENBY"], 191])
        elif number == '4':
            i2c.send_write([4, motor_pins["ENAX"], 255])
            i2c.send_write([4, motor_pins["ENBX"], 255])
            i2c.send_write([4, motor_pins["ENAY"], 255])
            i2c.send_write([4, motor_pins["ENBY"], 255])
        else: return {"success": False}
        return {"success": True}

api.add_resource(Drive, '/api/drive/<direction>')
api.add_resource(Sonar, '/api/sonar/all')
api.add_resource(Initialize, '/api/initialize')
api.add_resource(Lights, '/api/lights/<light>/<state>')
api.add_resource(Gear, '/api/gear/<number>')

if __name__ == "__main__":
    app.run(port='8500', host='0.0.0.0')
