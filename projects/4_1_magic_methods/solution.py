'''
Файл с магическими методами

https://www.coursera.org/learn/diving-in-python/programming/sypSV/fail-s-maghichieskimi-mietodami
'''

import os.path
import tempfile


class File:
    def __init__(self, path):
        self._path = path
        self._curr = 0

        if not os.path.exists(path):
            with open(self._path, 'w'):
                pass

    def __str__(self):
        return self._path

    def __iter__(self):
        with open(self._path, 'r', encoding='utf8') as f:
            self._lines = f.readlines()
        return self

    def __next__(self):
        try:
            line = self._lines[self._curr]
            self._curr += 1
            return line
        except IndexError:
            raise StopIteration

    def __add__(self, other):
        result_path = os.path.join(tempfile.gettempdir(), 'tmp.txt')
        result = File(result_path)
        result.write(self.read() + other.read())
        return result

    def read(self):
        with open(self._path, 'r', encoding='utf8') as f:
            return f.read()

    def write(self, text):
        with open(self._path, 'w', encoding='utf8') as f:
            f.write(text)


if __name__ == '__main__':
    pass
