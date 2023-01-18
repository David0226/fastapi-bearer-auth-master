from influxdb_client import InfluxDBClient
import config

def db_conn():
    dburl = config.dburl
    token = config.token
    org  = config.org

    client = InfluxDBClient(url=dburl, token=token, org=org)

    return client
