'''
Дескриптор с комиссией

Часто при зачислении каких-то средств на счет с нас берут комиссию.
Давайте реализуем похожий механизм с помощью дескрипторов.

Напишите дескриптор Value, который будет использоваться в нашем классе Account
'''


class Value:
    def __init__(self):
        self.value = 0

    def __set__(self, obj, value):
        self.value = value * (1 - obj.commission)

    def __get__(self, obj, obj_type):
        return self.value


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission


if __name__ == '__main__':
    pass
#    test:
#    acc = Account(0.1)
#    acc.amount = 100
#    print(acc.amount)
