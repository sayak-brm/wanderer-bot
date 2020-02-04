#! /usr/bin/python3
import json

from flask import Flask
from flask_restful import Api
from flask_restful import Resource
from i2cio import I2CIO
from gpsio import GPSIO

APP = Flask(__name__)
API = Api(APP)
I2C = I2CIO(0x01)
GPS = GPSIO()
APP.config["DEBUG"] = True

OPTS = ""
with open("params.json") as params:
    OPTS = json.loads(params.read())


class Drive(Resource):
    @staticmethod
    def post(direction):
        if direction in OPTS["dirs"]:
            I2C.send_write([6, OPTS["dirs"][direction]])
            return {"success": True}
        print("ERR: Incorrect Drive Direction")
        return {"success": False}


class Sonar(Resource):
    @staticmethod
    def get():
        I2C.send_write([0])
        return {"success": True, "sonar": I2C.send_read(3)}


class Lights(Resource):
    @staticmethod
    def post(light, state):
        if light in OPTS["lights"]:
            if state in OPTS["relay_ao"]:
                I2C.send_write(
                    [2, OPTS["lights"][light], OPTS["relay_ao"][state]])
                return {"success": True}
        return {"success": False}


class Gears(Resource):
    @staticmethod
    def post(number):
        if number in OPTS["gears"]:
            I2C.send_write([7, OPTS["gears"][number]])
            return {"success": True}
        return {"success": False}

class Navigation(Resource):
    @staticmethod
    def get(device):
        if device == "gps":
            return {"success": True, "gps": GPS.get_data()}
        return {"success": False}


API.add_resource(Drive, "/api/drive/<direction>")
API.add_resource(Sonar, "/api/sonar/all")
API.add_resource(Lights, "/api/lights/<light>/<state>")
API.add_resource(Gears, "/api/gear/<number>")
API.add_resource(Gears, "/api/navigation/<device>")

if __name__ == "__main__":
    APP.run(port="8500", host="0.0.0.0")
