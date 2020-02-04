import json

import gpsd


class GPSIO:
    def __init__(self):
        gpsd.connect()

    def get_data(self):
        packet = gpsd.get_current()
        data = {"Mode": packet.mode, "Sats": packet.sats}
        if packet.mode >= 2:
            data.update(
                Mode=packet.mode,
                Sats=packet.sats,
                Lat=packet.lat,
                Lon=packet.lon,
                Track=packet.track,
                Hspeed=packet.hspeed,
                Time=packet.time,
                Error=packet.error,
                Position_Precision=packet.position_precision(),
                Map_Url=packet.map_url(),
            )
        if packet.mode >= 3:
            data.update(Climb=packet.climb, Alt=packet.alt)
        return data
