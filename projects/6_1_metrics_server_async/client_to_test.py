"""
Это вспомогательный скрипт для тестирования сервера из задания на неделе 6.

Сначала запускаете ваш сервер на адресе 127.0.0.1 и порту 8888, а затем
запускаете этот скрипт.
"""

import sys
import bisect
import socket
import time


class ClientError(Exception):
    """класс исключений клиента"""
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

        try:
            self.connection = socket.create_connection((host, port), timeout)
        except socket.error as err:
            raise ClientError("Cannot create connection", err)

    def _read(self):

        data = b""

        while not data.endswith(b"\n\n"):
            try:
                data += self.connection.recv(1024)
            except socket.error as err:
                raise ClientError("Error reading data from socket", err)

        return data.decode('utf-8')

    def _send(self, data):

        try:
            self.connection.sendall(data)
        except socket.error as err:
            raise ClientError("Error sending data to server", err)

    def put(self, key, value, timestamp=None):

        timestamp = timestamp or int(time.time())
        self._send(f"put {key} {value} {timestamp}\n".encode())
        raw_data = self._read()

        if raw_data == 'ok\n\n':
            return
        raise ClientError('Server returns an error')

    def get(self, key):

        self._send(f"get {key}\n".encode())
        raw_data = self._read()
        data = {}
        status, payload = raw_data.split("\n", 1)
        payload = payload.strip()

        if status != 'ok':
            raise ClientError('Server returns an error')

        if payload == '':
            return data

        try:

            for row in payload.splitlines():
                key, value, timestamp = row.split()
                if key not in data:
                    data[key] = []
                bisect.insort(data[key], ((int(timestamp), float(value))))

        except Exception as err:
            raise ClientError('Server returns invalid data', err)

        return data

    def close(self):

        try:
            self.connection.close()
        except socket.error as err:
            raise ClientError("Error. Do not close the connection", err)


def run(host, port):
    client1 = Client(host, port, timeout=5)
    client2 = Client(host, port, timeout=5)
    command = "wrong command test\n"

    try:
        data = client1.get(command)
    except ClientError:
        pass
    except BaseException as err:
        print(f"Ошибка соединения с сервером: {err.__class__}: {err}")
        sys.exit(1)
    else:
        print("Неверная команда, отправленная серверу, должна возвращать ошибку протокола")
        sys.exit(1)

    command = 'some_key'
    try:
        data_1 = client1.get(command)
        data_2 = client1.get(command)
    except ClientError:
        print('Сервер вернул ответ на валидный запрос, который клиент определил, '
              'как не корректный.. ')
    except BaseException as err:
        print(f"Сервер должен поддерживать соединение с клиентом между запросами, "
              f"повторный запрос к серверу завершился ошибкой: {err.__class__}: {err}")
        sys.exit(1)

    assert data_1 == data_2 == {}, \
        "На запрос клиента на получения данных по не существующему ключу, сервер " \
        "вдолжен озвращать ответ с пустым полем данных."

    try:
        data_1 = client1.get(command)
        data_2 = client2.get(command)
    except ClientError:
        print('Сервер вернул ответ на валидный запрос, который клиент определил'
              ', как не корректный.. ')
    except BaseException as err:
        print(f"Сервер должен поддерживать соединение с несколькими клиентами: "
              f"{err.__class__}: {err}")
        sys.exit(1)

    assert data_1 == data_2 == {}, \
        "На запрос клиента на получения данных по не существующему ключу, сервер " \
        "должен возвращать ответ с пустым полем данных."

    try:
        client1.put("k1", 0.25, timestamp=1)
        client2.put("k1", 2.156, timestamp=2)
        client1.put("k1", 0.35, timestamp=3)
        client2.put("k2", 30, timestamp=4)
        client1.put("k2", 40, timestamp=5)
        client1.put("k2", 41, timestamp=5)
    except Exception as err:
        print(f"Ошибка вызова client.put(...) {err.__class__}: {err}")
        sys.exit(1)

    expected_metrics = {
        "k1": [(1, 0.25), (2, 2.156), (3, 0.35)],
        "k2": [(4, 30.0), (5, 41.0)],
    }

    try:
        metrics = client1.get("*")
        if metrics != expected_metrics:
            print(f"client.get('*') вернул неверный результат. Ожидается: "
                  f"{expected_metrics}. Получено: {metrics}")
            sys.exit(1)
    except Exception as err:
        print(f"Ошибка вызова client.get('*') {err.__class__}: {err}")
        sys.exit(1)

    expected_metrics = {"k2": [(4, 30.0), (5, 41.0)]}

    try:
        metrics = client2.get("k2")
        if metrics != expected_metrics:
            print(f"client.get('k2') вернул неверный результат. Ожидается: "
                  f"{expected_metrics}. Получено: {metrics}")
            sys.exit(1)
    except Exception as err:
        print(f"Ошибка вызова client.get('k2') {err.__class__}: {err}")
        sys.exit(1)

    try:
        result = client1.get("k3")
        if result != {}:
            print(
                f"Ошибка вызова метода get с ключом, который еще не был добавлен. "
                f"Ожидается: пустой словарь. Получено: {result}")
            sys.exit(1)
    except Exception as err:
        print(f"Ошибка вызова метода get с ключом, который еще не был добавлен: "
              f"{err.__class__} {err}")
        sys.exit(1)

    print("Похоже, что все верно! Попробуйте отправить решение на проверку.")


if __name__ == "__main__":
    run("127.0.0.1", 8888)
