from influxdb_client import InfluxDBClient
from dotenv import load_dotenv
import os

def influxdb_conn():
    load_dotenv()
    dburl = os.getenv('dburl')
    token = os.getenv('token')
    org  = os.getenv('org')
    client = InfluxDBClient(url=dburl, token=token, org=org)
    return client