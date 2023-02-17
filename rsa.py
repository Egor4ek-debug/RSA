from random import randint
# from math import gcd  # Поиск наименьшего общего делителя


# def is_prime(number):
#     if number < 2:
#         return False
#     return all(number % i != 0 for i in range(2, number))


# def primeNumber(digital=4):
#     while is_prime(digital) != True:
#         digital = randint(2, 1000)
#     return digital


# def decodeMessage(msg):
#     asciimessage = list(bytes(msg, 'utf-8'))
#     return [pow(i, e, n) for i in asciimessage]


# def encodedMessage():
#     arrayText = [chr(pow(i, d, n)) for i in decodeMessage(msg)]
#     return ''.join(arrayText)


# def get_e(e):
#     while gcd(phi_n, e) != 1:
#         e = randint(2, 1000)
#     return e


# def get_d(d):
#     while ((e*d) % phi_n != 1):
#         d += 1
#     return d


# p, q = primeNumber(), primeNumber()


# n = p*q
# phi_n = (p-1)*(q-1)

# e = get_e(0)

# d = get_d(int(phi_n/e))


# msg = input('Enter the text ')
# print(
#     f'Decoded messgae: {decodeMessage(msg)}\n You encoded message: {encodedMessage()} ')


class RSA:

    def __init__(self):
        self.p = self.primeNumber()
        self.q = self.primeNumber()
        self.n = self.p*self.q
        self.phi_n = (self.p-1)*(self.q-1)
        self.e = self.generate_e()
        self.d = self.generate_d()

    def checkPrime(self, number):
        if number < 2:
            return False
        return all(number % i != 0 for i in range(2, number))

    def primeNumber(self, digital=4):
        while self.checkPrime(digital) != True:
            digital = randint(2, 1000)
        return digital

    def generate_e(self):
        # Выбираем случайное целое число e, такое что 1 < e < phi_n и e взаимно просто с phi_n
        while True:
            e = randint(2, self.phi_n - 1)
            if self.gcd(e, self.phi_n) == 1:
                return e

    def generate_d(self):
        # Находим число d, такое что (e * d) mod phi_n = 1
        d = 1
        while True:
            if (self.e * d) % self.phi_n == 1:
                return d
            d += 1

    def gcd(self, x, y):
        if (y == 0):
            return x
        else:
            return self.gcd(y, x % y)

    def encrypt(self, message):
        # Шифруем сообщение m: c = m^e mod n
        asciimessage = list(bytes(message, 'utf-8'))
        return [pow(i, self.e, self.n) for i in asciimessage]

    def decrypt(self):
        # Расшифровываем зашифрованное сообщение c: m = c^d mod n
        arrayText = [chr(pow(i, self.d, self.n)) for i in self.encrypt(msg)]
        return ''.join(arrayText)

    def print(self):
        decryptText= [str(x) for x in self.encrypt(msg)]
        print(
            f'You encoded messgae: {"".join(decryptText)}\n You decoded message: {self.decrypt()} ')


rsa = RSA()
msg = input('Enter the text ')
rsa.print()
