import gpsd
import json


class GPSIO:
    def __init__(self):
        gpsd.connect()
        self.packet = gpsd.get_current()

    def get_mode(self):
        return self.packet.mode

    def get_satellites(self):
        return self.packet.sats

    def get_latlon(self):
        return (self.packet.lat, self.packet.lon)

    def get_track(self):
        return self.packet.track

    def get_hspeed(self):
        return self.packet.hspeed

    def get_time(self):
        return self.packet.time

    def get_error(self):
        return self.packet.error

    def get_climb(self):
        return self.packet.climb

    def get_alt(self):
        return self.packet.alt

    def get_position_precision(self):
        return self.packet.position_precision()

    def get_map_url(self):
        return self.packet.map_url()

    def get_json(self):
        jsonstring = {"Mode": self.packet.mode, "Sats": self.packet.sats}
        if self.packet.mode >= 2:
            jsonstring.update(
                Mode=self.packet.mode,
                Sats=self.packet.sats,
                Lat=self.packet.lat,
                Lon=self.packet.lon,
                Track=self.packet.track,
                Hspeed=self.packet.hspeed,
                Time=self.packet.time,
                Error=self.packet.error,
                Position_Precision=self.packet.position_precision(),
                Map_Url=self.packet.map_url(),
            )
        if self.packet.mode >= 3:
            jsonstring.update(Climb=self.packet.climb, Alt=self.packet.alt)
        return json.dumps(jsonstring)
