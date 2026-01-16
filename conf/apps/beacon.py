from appdaemon.plugins.hass.hassapi import Hass
import uptimekuma


class Beacon(Hass):
    def initialize(self):
        self.log('Initialized my app')
        self.indicator_light = self.args.get("light")

        self.uk = uptimekuma.UptimeKumaClient(
            url=self.args.get("uptimekuma_url"),
            username=self.args.get("username"),
            password=self.args.get("password")
        )

        self.run_every(self.do, "now", 5)

    def do(self, kwargs):
        monitors = self.uk.api.get_monitors()
        self.log(f"Uptime Kuma Monitors: {len(monitors)} monitors found")
        self.turn_on(self.indicator_light, rgb_color=[255, 0, 0])