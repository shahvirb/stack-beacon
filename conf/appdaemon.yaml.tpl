appdaemon:
  import_method: expert 
  latitude: 0
  longitude: 0
  elevation: 0
  time_zone: America/Chicago
  plugins: 
    HASS:
      type: hass
      ha_url: http://homeassistant.fdatxvault.win:8123 
      token: op://Dev - Home Lab/Home Assistant/beacon token
    # MQTT:
    #   type: mqtt
    #   namespace: beacon
    #   client_host: http://homeassistant.fdatxvault.win
    #   # client_port: 1883
    #   client_user: beacon
    #   client_password: op://Dev - Home Lab/Home Assistant/beacon mqtt password
    #   client_topics:
    #     - zigbee2mqtt/#
http:
  url: http://0.0.0.0:5050