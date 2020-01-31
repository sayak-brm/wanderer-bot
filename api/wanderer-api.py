#! /usr/bin/python3
from flask import Flask
from flask_restful import Api
from flask_restful import Resource
from i2cio import I2CIO

app = Flask(__name__)
api = Api(app)
i2c = I2CIO(0x01)
app.config["DEBUG"] = True

relay_pins = {"DRL": 37, "DIP": 39}


class Drive(Resource):
    def post(self, direction):
        if direction == "front":
            i2c.send_write([6, 1])
        elif direction == "back":
            i2c.send_write([6, 2])
        elif direction == "left":
            i2c.send_write([6, 3])
        elif direction == "right":
            i2c.send_write([6, 4])
        elif direction == "stop":
            i2c.send_write([6, 5])
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
        if state == "on":
            i2c.send_write([2, relay_pins["DRL"], 0])
        if state == "off":
            i2c.send_write([2, relay_pins["DRL"], 1])

    @staticmethod
    def dip(state):
        if state == "on":
            i2c.send_write([2, relay_pins["DIP"], 0])
        if state == "off":
            i2c.send_write([2, relay_pins["DIP"], 1])

    def post(self, light, state):
        if light == "drl":
            Lights.drl(state)
        if light == "dip":
            Lights.dip(state)


class Gear(Resource):
    def post(self, number):
        if number == "1":
            i2c.send_write([7, 63])
        elif number == "2":
            i2c.send_write([7, 127])
        elif number == "3":
            i2c.send_write([7, 191])
        elif number == "4":
            i2c.send_write([7, 255])
        else:
            return {"success": False}
        return {"success": True}


api.add_resource(Drive, "/api/drive/<direction>")
api.add_resource(Sonar, "/api/sonar/all")
api.add_resource(Lights, "/api/lights/<light>/<state>")
api.add_resource(Gear, "/api/gear/<number>")

if __name__ == "__main__":
    app.run(port="8500", host="0.0.0.0")
