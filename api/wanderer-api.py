#! /usr/bin/python3
import json
from flask import Flask
from flask_restful import Api
from flask_restful import Resource
from i2cio import I2CIO

app = Flask(__name__)
api = Api(app)
i2c = I2CIO(0x01)
app.config["DEBUG"] = True

opts = ''
with open('params.json') as params:
    opts = json.loads(params.read())

class Drive(Resource):
    def post(self, direction):
        if direction in opts["dirs"]:
            i2c.send_write([6,  opts["dirs"][direction]])
            return {"success": True}
        print("ERR: Incorrect Drive Direction")
        return {"success": False}

class Sonar(Resource):
    def get(self):
        i2c.send_write([0])
        return i2c.send_read(3)


class Lights(Resource):
    def post(self, light, state):
        if light in opts["lights"]:
            if state in opts["relay_ao"]:
                i2c.send_write([2, opts["lights"][light],
                    opts["relay_ao"][state]])
                return {"success": True}
        return {"success": False}

class Gears(Resource):
    def post(self, number):
        if number in opts["gears"]:
            i2c.send_write([7,  opts["gears"][number]])
            return {"success": True}
        return {"success": False}

api.add_resource(Drive, '/api/drive/<direction>')
api.add_resource(Sonar, '/api/sonar/all')
api.add_resource(Lights, '/api/lights/<light>/<state>')
api.add_resource(Gears, '/api/gear/<number>')

if __name__ == "__main__":
    app.run(port="8500", host="0.0.0.0")
