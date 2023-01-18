from database.dbconn import db_conn


conn = db_conn()
print(conn.health())