import logging
from uptime_kuma_api import UptimeKumaApi
from uptime_kuma_api import MonitorStatus

class StatusPageParser:
    def __init__(self, status_page_data):
        self.data = status_page_data
    
    def get_groups(self):
        """Returns list of all groups with their metadata."""
        return [{'id': g['id'], 'name': g['name'], 'weight': g['weight']} 
                for g in self.data]
    
    def get_monitors(self, group_id=None):
        """Returns monitors, optionally filtered by group_id."""
        monitors = []
        for group in self.data:
            if group_id is None or group['id'] == group_id:
                for monitor in group.get('monitorList', []):
                    monitors.append({
                        'group_id': group['id'],
                        'group_name': group['name'],
                        **monitor
                    })
        return monitors
    
    def get_monitor_count(self):
        """Returns total number of monitors."""
        return sum(len(g.get('monitorList', [])) for g in self.data)
    
    def get_stats(self):
        """Returns summary statistics."""
        return {
            'total_groups': len(self.data),
            'total_monitors': self.get_monitor_count(),
            'groups': [
                {
                    'name': g['name'],
                    'monitor_count': len(g.get('monitorList', []))
                }
                for g in self.data
            ]
        }

    def get_monitor_ids_and_names(self):
        """Returns list of all monitor IDs and names."""
        result = []
        for group in self.data:
            for monitor in group.get('monitorList', []):
                result.append({
                    'id': monitor['id'],
                    'name': monitor['name']
                })
        return result

class UptimeKumaClient:
    def __init__(self, url, username, password):
        self.api = UptimeKumaApi(url)
        self.api.login(username, password)
        logging.info(f"Logged into Uptime Kuma at {url}")

    def get_status_page(self, page_name="beacon"):
        status_page_data = self.api.get_status_page(page_name)
        return StatusPageParser(status_page_data['publicGroupList'])

    def get_relevant_monitors(self):
        status_page = self.get_status_page()
        monitors = status_page.get_monitor_ids_and_names()
        for monitor in monitors:
            status_value = self.api.get_monitor_status(monitor['id'])
            monitor['status'] = MonitorStatus(status_value).name.lower()
            # logging.info(f"Monitor {monitor['name']} (ID: {monitor['id']}) status: {monitor['status']}")
        return monitors
