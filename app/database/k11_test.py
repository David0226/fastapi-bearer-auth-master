from influxdb_client import InfluxDBClient
# Import client library classes.
from influxdb_client import Authorization, InfluxDBClient, Permission, PermissionResource, Point, WriteOptions
from influxdb_client.client.authorizations_api import AuthorizationsApi
from influxdb_client.client.bucket_api import BucketsApi
from influxdb_client.client.query_api import QueryApi
from influxdb_client.client.write_api import SYNCHRONOUS


from dotenv import load_dotenv
import os
from typing import Dict


print("start")
load_dotenv()
url = os.getenv('url')
token = "Token Id0RgECCkJKOjKk1eyDKG-s9pyR69Wv7QekequNfQQd90meX95yb1FTE2YuwF3wQm-6oStShhaj_suumiJS1Eg=="
org = os.getenv('org')
influxdb_client = InfluxDBClient(url=url,
                        token=token, 
                        org=org)
print("health check: ", influxdb_client.health())
query_api = QueryApi(influxdb_client)

query = 'from(bucket: "k11") \
        |> range(start: -3h) \
        |> filter(fn: (r) => r._measurement == "cell")\
        |> filter(fn: (r) => r.bank_idx == "0")\
        |> filter(fn: (r) => r._field == "soc")'

result = query_api.query(query=query)
print("result", result)
results = []
columns = []

for table in result:  # FluxTable for each result field
    for record in table.records:
        results.append((record.get_value(), record.get_field()))

print(result)


def get_device(device_id=None) -> {}:
    influxdb_client = InfluxDBClient(url=config.get('APP', 'INFLUX_URL'),
                                     token=os.environ.get('INFLUX_TOKEN'),
                                     org=os.environ.get('INFLUX_ORG'))
    # Queries must be formatted with single and double quotes correctly
    query_api = QueryApi(influxdb_client)
    device_filter = ''
    if device_id:
        device_id = str(device_id)
        device_filter = f'r.deviceId == "{device_id}" and r._field != "token"'
    else:
        device_filter = f'r._field != "token"'

    flux_query = f'from(bucket: "{config.get("APP", "INFLUX_BUCKET_AUTH")}") ' \
                 f'|> range(start: 0) ' \
                 f'|> filter(fn: (r) => r._measurement == "deviceauth" and {device_filter}) ' \
                 f'|> last()'
    
    response = query_api.query(flux_query)
    result = []
    for table in response:
        for record in table.records:
            try:
                'updatedAt' in record
            except KeyError:
                record['updatedAt'] = record.get_time()
                record[record.get_field()] = record.get_value()
            result.append(record.values)
    return result