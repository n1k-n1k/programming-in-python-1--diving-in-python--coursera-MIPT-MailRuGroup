"""
Клиент для отправки метрик
https://www.coursera.org/learn/diving-in-python/programming/aG3x3/kliient-dlia-otpravki-mietrik
"""

import socket
import time


class ClientError(Exception):
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        self._host = host
        self._port = port
        self._timeout = timeout
        try:
            self._sock = socket.create_connection((self._host, self._port), self._timeout)
        except socket.error as err:
            raise ClientError(err)

    def put(self, metric_key, metric_value, timestamp=None):
        timestamp = str(timestamp or int(time.time()))
        send_data = f'put {metric_key} {metric_value} {timestamp}\n'.encode('utf8')

        try:
            self._sock.sendall(send_data)
            response = self._sock.recv(1024)
            if b'ok\n' not in response:
                raise ClientError
        except Exception:
            raise ClientError

    def get(self, key):
        metric_dict = {}
        send_data = f'get {key}\n'.encode('utf8')

        try:
            self._sock.sendall(send_data)
            response = self._sock.recv(1024)
            if b'ok' not in response:
                raise ClientError

            response = str(response).strip('\n').split('\\n')

            for m in response:
                metrics = m.split(' ')
                if len(metrics) == 3:
                    metric_key = metrics[0]
                    metric_value = float(metrics[1])
                    metric_timestamp = int(metrics[2])
                    metric_list = metric_dict.get(metric_key, [])
                    metric_list.append((metric_timestamp, metric_value))
                    metric_dict.update({metric_key: sorted(metric_list)})
                elif metrics not in [["b'ok"], [""], ["'"]]:
                    raise ClientError

            return metric_dict

        except Exception as err:
            raise ClientError(err)


if __name__ == '__main__':
    client = Client('127.0.0.1', 8888, timeout=15)
    print(client.get('*'))
