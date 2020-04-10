"""
Асинхронный сервер для приема метрик
https://www.coursera.org/learn/diving-in-python/programming/Xcdpa/siervier-dlia-priiema-mietrik
"""

import asyncio


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = process_data(data.decode())
        self.transport.write(resp.encode())


def process_data(data):
    pass


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


metrics = dict()

if __name__ == '__main__':
    run_server('127.0.0.1', 8888)
