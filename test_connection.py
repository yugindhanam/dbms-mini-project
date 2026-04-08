import oracledb

connection = oracledb.connect(
    user="system",
    password="",
    dsn="localhost/XEPDB1"
)

print("Connected to Oracle Database")

connection.close()