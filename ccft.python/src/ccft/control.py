from ccft.conn.base_conn import AbstConn

server: AbstConn


def heartbeat():
    if server is not None:
        server.send()
