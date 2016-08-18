import json
import httplib
import random


import logging

httplib.HTTPConnection.debuglevel = 1
# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def parse_config():
    return json.load(open('config.json'))


def main():
    configs = parse_config()
    host = configs.get('host', 'localhost')
    port = configs.get('port', 80)
    path = "/api/external/v1/sensors/%(sensor_id)s/sensordata/" % configs

    connection = httplib.HTTPConnection(host, port, timeout=2)

    headers = {
        "Content-type": "application/vnd.api+json",
        "ORGANIZATION-ID": configs.get("organization_id"),
        "ORGANIZATION-API-KEY": configs.get("organization_api_key")
    }

    body = json.dumps({
        "data": {
            "id": None,
            "type": "SensorData",
            "attributes": {
                "timestamp": "2016-05-12T13:08:46.101226Z",
                "value": random.randint(0, 100)
            },
            "relationships": {
                "sensor": {
                    "data": {
                        "type": "Sensor",
                        "id": configs.get('sensor_id')
                    }
                }
            }
        }
    })

    connection.request("POST", path, body, headers)
    response = connection.getresponse()

    print response.read()

if __name__ == "__main__":
    main()
