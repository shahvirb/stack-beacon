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

        self.run_every(self.do, "now", 3)

    def do(self, kwargs):
        monitors = self.uk.api.get_monitors()
        # self.log(f"Uptime Kuma Monitors: {len(monitors)} monitors found")
        # page = self.uk.api.get_status_page("beacon")
        # self.log(f"Uptime Kuma Status Page: {page['publicGroupList']}")

        monitors = self.uk.get_relevant_monitors()
        up_count = sum(1 for m in monitors if m.get('status') == 'up')
        total_count = len(monitors)
        self.log(f"uptime kuma monitors: {up_count}/{total_count} are up")

        percentage = up_count / total_count if total_count > 0 else 0
        if percentage == 1.0:
            color_name = "green"
        elif percentage == 0.0:
            color_name = "red"
        else:
            color_name = "yellow"

        self.turn_on(self.indicator_light, color_name=color_name)