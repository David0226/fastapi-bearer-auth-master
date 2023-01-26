from pydoc import cli
from typing import Dict
from unittest import result
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from database import db_conn
import json
from datetime import datetime


client = db_conn.influxdb_conn()
query_api = client.query_api()


def read_root():

    query = ' from(bucket: "garak")\
    |> range(start: -7d)\
    |> filter(fn: (r) => r["_measurement"] == "module_volt")\
    |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)\
    |> yield(name: "mean")'

    result = client.query_api().query(query, org='codiplay')
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_value(), record.get_field()))

    return {'results': results}


def read_racks():

    query = ' from(bucket: "k11") \
        |> range(start: 2022-03-21T02:00:00Z, stop: 2022-12-31T14:59:59.999Z) \
        |> filter(fn: (r) => r["_measurement"] == "rack") \
        |> filter(fn: (r) => r["bank_idx"] == "0") \
        |> filter(fn: (r) => r["rack_idx"] == "0") \
        |> filter(fn: (r) => r["_field"] == "alarm" or r["_field"] == "assembled" or r["_field"] == "created" or r["_field"] == "cur" or r["_field"] == "soc" or r["_field"] == "soh" or r["_field"] == "status" or r["_field"] == "vol") \
        |> top(n:10, columns: ["_value"]) \
    '

    # |> keep(columns: ["_value", "_time", "_field"]) \

    result = client.query_api().query(query)

    results = []
    columns = []

    for table in result:  # FluxTable for each result field
        for record in table.records:
            results.append((record.get_value(), record.get_field()))

    return {'results': results}


def read_racks_as_csv():

    query = ' from(bucket: "k11") \
        |> range(start: 2022-03-21T02:00:00Z, stop: 2022-12-31T14:59:59.999Z) \
        |> filter(fn: (r) => r["_measurement"] == "rack") \
        |> filter(fn: (r) => r["bank_idx"] == "0") \
        |> filter(fn: (r) => r["rack_idx"] == "0") \
        |> filter(fn: (r) => r["_field"] == "alarm" or r["_field"] == "assembled" or r["_field"] == "created" or r["_field"] == "cur" or r["_field"] == "soc" or r["_field"] == "soh" or r["_field"] == "status" or r["_field"] == "vol") \
        |> aggregateWindow(every: 10m, fn: mean, createEmpty: false) \
        |> top(n:10) \
    '

    # |> keep(columns: ["_value", "_time", "_field"]) \

    results = query_api.query_csv(query, org='codiplay')

    for line in results:  # FluxTable for each result field
        print(line)

    return {'results': results}


def read_racks_as_df():

    query = ' from(bucket: "k11") \
        |> range(start: 2022-03-21T02:00:00Z, stop: 2022-12-31T14:59:59.999Z) \
        |> filter(fn: (r) => r["_measurement"] == "rack") \
        |> filter(fn: (r) => r["bank_idx"] == "0") \
        |> filter(fn: (r) => r["rack_idx"] == "0") \
        |> filter(fn: (r) => r["_field"] == "alarm" or r["_field"] == "assembled" or r["_field"] == "created" or r["_field"] == "cur" or r["_field"] == "soc" or r["_field"] == "soh" or r["_field"] == "status" or r["_field"] == "vol") \
        |> top(n:10, columns: ["_value"]) \
    '

    # |> keep(columns: ["_value", "_time", "_field"]) \

    results = query_api.query_data_frame(query, org='codiplay')

    for line in results:  # FluxTable for each result field
        print(line)

    return {'results': results}


def read_racks_mean_as_csv():

    query = ' from(bucket: "k11") \
        |> range(start: 2022-03-21T02:00:00Z, stop: 2022-12-31T14:59:59.999Z) \
        |> filter(fn: (r) => r["_measurement"] == "rack") \
        |> filter(fn: (r) => r["bank_idx"] == "0") \
        |> filter(fn: (r) => r["rack_idx"] == "0") \
        |> filter(fn: (r) => r["_field"] == "cur" or r["_field"] == "vol") \
        |> aggregateWindow(every: 1m, fn: mean, createEmpty: false) \
        |> yield(name: "mean")'

    results = query_api.query_csv(query)

    for line in results:
        print(line)

    return {'results': results}


def read_root_as_table():

    query = ' from(bucket: "k11") \
        |> range(start: 2022-03-21T02:00:00Z, stop: 2022-12-31T14:59:59.999Z) \
        |> filter(fn: (r) => r["_measurement"] == "rack") \
        |> filter(fn: (r) => r["bank_idx"] == "0") \
        |> filter(fn: (r) => r["rack_idx"] == "0") \
        |> filter(fn: (r) => r["_field"] == "cur" or r["_field"] == "vol", or r["_field"] == "") \
        |> aggregateWindow(every: 1m, fn: mean, createEmpty: false) \
        |> yield(name: "mean")'

    results = query_api.query(query, org='codiplay')
    result_list = []
    columns = []

    for table_idx, table in enumerate(results):
        columns.append(table.records[0].get_field())
        columns.append(table.records[0].get_field() + '_time')
        for record_idx, record in enumerate(table.records):

            if len(result_list) < record_idx + 1:
                result_list.append([])
            result_record = result_list[record_idx]
            result_record.append(record.get_value())
            result_record.append(record.values["_time"])

    return {'results': {'columns': columns, 'data': result_list}}


def read_cell_as_table():
    query = 'from(bucket: "k11")\
        |> range(start: 2022-03-20T02:00:00Z, stop: 2022-12-31T14:59:59.999Z) \
        |> filter(fn: (r) => r["_measurement"] == "cell")\
        |> filter(fn: (r) => r["bank_idx"] == "0")\
        |> filter(fn: (r) => r["rack_idx"] == "0")\
        |> filter(fn: (r) => r["modu_idx"] == "0")\
        |> filter(fn: (r) => r["cell_idx"] == "0")\
        |> filter(fn: (r) => r["_field"] == "soc" or r["_field"] == "soh" or r["_field"] == "vol" or r["_field"] == "assembled" or r["_field"] == "created")\
        |> aggregateWindow(every: 10m, fn: mean, createEmpty: false)\
        |> yield(name: "mean")'

    results = query_api.query(query, org='codiplay')
    result_list = []
    columns = []
    time_appended = False
    time_column_appended = False
    for table_idx, table in enumerate(results):
        if not time_column_appended:
            columns.append('_time')
            time_column_appended = True

        columns.append(table.records[0].get_field())
        for record_idx, record in enumerate(table.records):

            if len(result_list) < record_idx + 1:
                result_list.append([])

            result_record = result_list[record_idx]

            if not time_appended:
                result_record.append(record.values["_time"])

            result_record.append(record.get_value())

        time_appended = True

    return {'results': {'columns': columns, 'data': result_list}}


def read_cell():
    query = 'from(bucket: "k11")\
        |> range(start: 2022-03-20T02:00:00Z, stop: 2022-12-31T14:59:59.999Z) \
        |> filter(fn: (r) => r["_measurement"] == "cell")\
        |> filter(fn: (r) => r["bank_idx"] == "0")\
        |> filter(fn: (r) => r["modu_idx"] == "0")\
        |> filter(fn: (r) => r["rack_idx"] == "0")\
        |> filter(fn: (r) => r["_field"] == "vol")\
        |> aggregateWindow(every: 10m, fn: last, createEmpty: false)\
        |> yield(name: "last")'

    results = query_api.query(query, org='codiplay')
    res = []

    for table_idx, table in enumerate(results):
        data = dict()
        data["x"] = []
        data["y"] = []
        for record_idx, record in enumerate(table.records):
            data["x"].append(
                datetime.strftime(record.values["_time"],
                                  '%Y-%m-%dT%H:%M:%SZ'))
            # data["x"].append(record.values["_time"])
            # data["x"].append(record_idx)
            data["y"].append(record.get_value())
        res.append(data)

    return {'results': res}


def read_bank_summary():
    query = 'from(bucket: "k11")\
        |> range(start: 2022-03-21T00:00:00Z, stop: 2022-03-23T22:00:00Z )\
        |> filter(fn: (r) => r["_measurement"] == "rack")\
        |> filter(fn: (r) => r["_field"] == "vol")\
        |> group(columns: ["bank_idx"])\
        |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)\
        |> yield(name: "mean")'

    results = query_api.query(query)
    res = []
    for table_idx, table in enumerate(results):
        data = dict()
        data["x"] = []
        data["y"] = []

        for record_idx, record in enumerate(table.records):
            date_str = datetime.strftime(record.values["_time"],
                                         '%Y-%m-%dT%H:%M:%SZ')
            data["x"].append(date_str)
            data["y"].append(record.get_value())
        res.append(data)

    return {'results': res}


def read_bank_summary_cur():
    query = 'from(bucket: "k11")\
        |> range(start: 2022-03-21T00:00:00Z, stop: 2022-03-23T22:00:00Z )\
        |> filter(fn: (r) => r["_measurement"] == "rack")\
        |> filter(fn: (r) => r["_field"] == "cur")\
        |> group(columns: ["bank_idx"])\
        |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)\
        |> yield(name: "mean")'

    results = query_api.query(query)
    res = []
    for table_idx, table in enumerate(results):
        data = dict()
        data["x"] = []
        data["y"] = []

        for record_idx, record in enumerate(table.records):
            date_str = datetime.strftime(record.values["_time"],
                                         '%Y-%m-%dT%H:%M:%SZ')
            data["x"].append(date_str)
            data["y"].append(record.get_value())
        res.append(data)

    return {'results': res}


def read_bank_summary_soc():
    query = 'from(bucket: "k11")\
        |> range(start: 2022-03-21T00:00:00Z, stop: 2022-03-23T22:00:00Z )\
        |> filter(fn: (r) => r["_measurement"] == "rack")\
        |> filter(fn: (r) => r["_field"] == "soc")\
        |> group(columns: ["bank_idx"])\
        |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)\
        |> yield(name: "mean")'

    results = query_api.query(query)
    res = []
    for table_idx, table in enumerate(results):
        data = dict()
        data["x"] = []
        data["y"] = []

        for record_idx, record in enumerate(table.records):
            date_str = datetime.strftime(record.values["_time"],
                                         '%Y-%m-%dT%H:%M:%SZ')
            data["x"].append(date_str)
            data["y"].append(record.get_value())
        res.append(data)

    return {'results': res}


def read_cells_for_histogram(bank_idx):
    print(bank_idx)
    query = f'from(bucket: "k11")\
        |> range(start: 2022-03-21T03:00:00Z, stop: 2022-03-21T22:00:00Z)\
        |> filter(fn: (r) => r["_measurement"] == "cell")\
        |> filter(fn: (r) => r["_field"] == "vol")\
        |> filter(fn: (r) => r["bank_idx"] == "{bank_idx}")\
        |> last()'

    results = query_api.query(query)
    res = []
    for table_idx, table in enumerate(results):
        for record_idx, record in enumerate(table.records):
            item = {
                "bank_idx": record.values["bank_idx"],
                "rack_idx": record.values["rack_idx"],
                "modu_idx": record.values["modu_idx"],
                "cell_idx": record.values["cell_idx"],
                "val": record.values["_value"],
            }
            res.append(item)

    return {'results': res}


# 20220420 hjh added start
def read_rack_status(bank_idx, rack_idx):

    query = f'from(bucket: "k11")\
        |> range(start:-5m, stop: now()) \
        |> filter(fn: (r) => r["_measurement"] == "rack")\
        |> filter(fn: (r) => r["bank_idx"] == "{bank_idx}")\
        |> filter(fn: (r) => r["rack_idx"] == "{rack_idx}")\
        |> aggregateWindow(every: 10m, fn: last, createEmpty: false)\
        |> last()'

    results = query_api.query(query, org='nemo')
    result_list = []
    columns = []
    time_appended = False
    time_column_appended = False
    for table_idx, table in enumerate(results):

        if not time_column_appended:
            columns.append('_time')
            time_column_appended = True
        columns.append(table.records[0].get_field())
        for record_idx, record in enumerate(table.records):

            if len(result_list) < record_idx + 1:
                result_list.append([])

            result_record = result_list[record_idx]

            if not time_appended:
                result_record.append(record.values["_time"])

            result_record.append(record.get_value())

        time_appended = True
    
    return {'results': {'columns': columns, 'data': result_list}}


def read_module_status(bank_idx, rack_idx):

    query = f'from(bucket: "k11")\
        |> range(start:-5m, stop: now()) \
        |> filter(fn: (r) => r["_measurement"] == "module") \
        |> filter(fn: (r) => r["_field"] == "assembled" or r["_field"] == "created" or r["_field"] == "module_bal1" or r["_field"] == "module_bal2" or r["_field"] == "module_pcbt1" or r["_field"] == "module_pcbt2" or r["_field"] == "module_vol1" or r["_field"] == "module_vol2" or r["_field"] == "module_vol3" or r["_field"] == "module_vol4" or r["_field"] == "temperature1" or r["_field"] == "temperature2" or r["_field"] == "temperature3" or r["_field"] == "temperature5" or r["_field"] == "temperature4" or r["_field"] == "temperature6")\
        |> filter(fn: (r) => r["bank_idx"] == "{bank_idx}") \
        |> filter(fn: (r) => r["modu_idx"] == "0" or r["modu_idx"] == "1" or r["modu_idx"] == "2" or r["modu_idx"] == "3" or r["modu_idx"] == "4" or r["modu_idx"] == "5") \
        |> filter(fn: (r) => r["rack_idx"] == "{rack_idx}") \
        |> aggregateWindow(every: 10m, fn: last, createEmpty: false)\
        |> last()'

    results = query_api.query(query, org='nemo')
    result_list = []
    columns = []
    time_appended = False
    time_column_appended = False
    for table_idx, table in enumerate(results):
        if not time_column_appended:
            columns.append('_time')
            time_column_appended = True
        
        columns.append(table.records[0].get_field())
        for record_idx, record in enumerate(table.records):

            if len(result_list) < record_idx + 1:
                result_list.append([])

            result_record = result_list[record_idx]

            if not time_appended:
                result_record.append(record.values["_time"])

            result_record.append(record.get_value())

        time_appended = True
    return {'results': {'columns': columns, 'data': result_list}}


def read_cell_status(bank_idx, rack_idx, val_type):
    # print("cell!!")
    # print(val_type)
    query = f'from(bucket: "k11")\
        |> range(start:-5m, stop: now()) \
        |> filter(fn: (r) => r["_measurement"] == "cell") \
        |> filter(fn: (r) => r["_field"] == "{val_type}") \
        |> filter(fn: (r) => r["bank_idx"] == "{bank_idx}") \
        |> filter(fn: (r) => r["rack_idx"] == "{rack_idx}") \
        |> aggregateWindow(every: 10m, fn: last, createEmpty: false)\
        |> last()'

    results = query_api.query(query, org='nemo')
    result_list = []
    columns = []
    time_appended = False
    time_column_appended = False
    for table_idx, table in enumerate(results):
        # print(table)
        if not time_column_appended:
            columns.append('_time')
            time_column_appended = True
        
        columns.append(table.records[0].get_field())
        # print(columns)
        for record_idx, record in enumerate(table.records):

            if len(result_list) < record_idx + 1:
                result_list.append([])

            result_record = result_list[record_idx]

            if not time_appended:
                result_record.append(record.values["_time"])

            result_record.append(record.get_value())

        time_appended = True
        # print(columns)
        # print(result_record)
    return {'results': {'columns': columns, 'data': result_list}}
# hjh added end