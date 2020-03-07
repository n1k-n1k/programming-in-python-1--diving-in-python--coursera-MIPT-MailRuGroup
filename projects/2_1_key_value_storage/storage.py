'''
Key-value хранилище

Утилита может вызваться со следующими параметрами:
Вывести на экран из хранилища значения по ключу:
--key <имя ключа> , где <имя ключа> - ключ по которому получаются значения.
Записать в хранилище значения по ключу:
--key <имя ключа> --val <значение>, где <значение> - сохраняемое значение.
'''

import os
import tempfile
import json
import argparse


def storage_data_get():
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    if os.path.exists(storage_path):
        with open(storage_path, 'r', encoding='utf8') as f:
            json_data = json.load(f)
            return json_data


def storage_data_put(data_dict):
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    with open(storage_path, 'w', encoding='utf8') as f:
        json.dump(data_dict, f)


def val_add(k, v):
    data = storage_data_get() or dict()
    if k in data:
        data[k].append(v)
    else:
        data[k] = [v]
    storage_data_put(data)


def val_get(k):
    data = storage_data_get()
    if data is not None and k in data:
        print(*data[k], sep=', ')
        return data[k]
    else:
        print(None)
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key')
    parser.add_argument('-v', '--val')
    args = parser.parse_args()
    k = args.key
    v = args.val
    if k and v:
        val_add(k, v)
    elif k:
        val_get(k)


if __name__ == '__main__':
    main()
