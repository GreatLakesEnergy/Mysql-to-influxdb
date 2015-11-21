import argparse

from influxdb import InfluxDBClient


def main(host='localhost', port=8086):
    user = 'root'
    password = 'gle12345'
    dbname = 'example'
    dbuser = 'sesh'
    dbuser_password = 'my_secret_password'
    query = 'select value from cpu_load_short;'
    """
    json_body = [
        {
            "measurement": "cpu_load_short",
            "tags": {
                "host": "server01",
                "region": "us-west"
            },
            "time": "2009-11-10T23:00:00Z",
            "fields": {
                "value": 0.64
            }
        }
    ]
    """
    """
    json_body = [
         {'fields': {
                    'value': 0.0
                    },
          'tags': {
                    'source': 'wago',
                     'site_name': 'Nyange'
                    },
         'time': '2015-11-05T07:39:41Z',
         'measurement': 'rTotalApparentPower'}
    ]
    """
    json_body =  [{'fields': {'value': 0.0}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'rTotalActiveEnergy'}, {'fields': {'value': 0.0}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'rTotalReactiveEnergy'}, {'fields': {'value': 0.0}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'DCPower2'}, {'fields': {'value': 2.0}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'DCPower1'}, {'fields': {'value': 9.0}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'DCVolt1'}, {'fields': {'value': 0.0}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'arVoltage_L_N2'}, {'fields': {'value': 9.0}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'arVoltage_L_N1'}, {'fields': {'value': 0.0}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'DCVolt2'}, {'fields': {'value': 0.0}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'arVoltage_L_N3'}, {'fields': {'value': 0}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'xRotatingField'}, {'fields': {'value': 0.0}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'rTotalApparentEnergy'}, {'fields': {'value': 0.0}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'arFrequency3'}, {'fields': {'value': 0.0}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'arFrequency2'}, {'fields': {'value': 0.0}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'arFrequency1'}, {'fields': {'value': datetime.datetime(2015, 11, 5, 7, 39, 41)}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'timestamp'}, {'fields': {'value': 3.0}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'rTotalActivePower'}, {'fields': {'value': 0.0}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'arCurrent2'}, {'fields': {'value': 0.0}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'arCurrent3'}, {'fields': {'value': 9.0}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'arCurrent1'}, {'fields': {'value': 1000L}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'iSiteCode'}, {'fields': {'value': 3.0}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'rTotalReactivePower'}, {'fields': {'value': 0L}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'trans'}, {'fields': {'value': 0.0}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'DCCurr2'}, {'fields': {'value': 10.0}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'DCCurr1'}, {'fields': {'value': 0.0}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'rTotalPowerFactorPF'}, {'fields': {'value': 0.0}, 'tags': {'source': 'wago', 'site_name': 'Nyange'}, 'time': '2015-11-05T07:39:41Z', 'measurement': 'rTotalApparentPower'}]


    client = InfluxDBClient(host, port, user, password, dbname)

    print("Create database: " + dbname)
    client.create_database(dbname)

    print("Create a retention policy")
    client.create_retention_policy('awesome_policy', '3d', 3, default=True)

    print("Switch user: " + dbuser)
    client.switch_user(dbuser, dbuser_password)

    print("Write points: {0}".format(json_body))
    client.write_points(json_body)

    print("Queying data: " + query)
    result = client.query(query)

    print("Result: {0}".format(result))

    print("Switch user: " + user)
    client.switch_user(user, password)

    print("Drop database: " + dbname)
    client.drop_database(dbname)


def parse_args():
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False, default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port)
