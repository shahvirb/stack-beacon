import logging
from uptime_kuma_api import UptimeKumaApi

class UptimeKumaClient:
    def __init__(self, url, username, password):
        self.api = UptimeKumaApi(url)
        self.api.login(username, password)
        logging.info(f"Logged into Uptime Kuma at {url}")