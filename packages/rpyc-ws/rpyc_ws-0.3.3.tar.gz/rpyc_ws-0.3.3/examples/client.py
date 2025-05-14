from rpyc_ws import connect_ws

with connect_ws("ws://localhost:8000/rpyc-ws/") as conn:
    print(conn.modules.os.getcwd())

# or

conn = connect_ws("ws://localhost:8000/rpyc-ws/")
print(conn.modules.os.getcwd())
conn.close()
