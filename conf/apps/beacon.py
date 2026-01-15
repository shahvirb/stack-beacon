from appdaemon.plugins.hass.hassapi import Hass

class Beacon(Hass):
    def initialize(self):
        self.log('Initialized my app')
        self.indicator_light = self.args.get("light")

        self.run_every(self.do, "now", 5)

    def do(self, kwargs):
        self.turn_on(self.indicator_light, rgb_color=[255, 0, 0])