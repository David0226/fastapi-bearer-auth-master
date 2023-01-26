from def_custom.dbconn import influxdb_conn


conn = dbconn.influxdb_conn()
print(conn.health())