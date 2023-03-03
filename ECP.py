import hashlib
import random


class RSA:
    def __init__(self, key_size=2048):
        # Генерируем пару ключей RSA
        self.n, self.e, self.d = self.generate_keypair(key_size)

    def generate_keypair(self, key_size):
        # Генерируем p и q
        p = self.generate_prime(key_size // 2)
        q = self.generate_prime(key_size // 2)

        # Вычисляем n
        n = p * q

        # Вычисляем функцию Эйлера от n
        phi_n = (p - 1) * (q - 1)

        # Выбираем открытую экспоненту e
        e = 65537

        # Вычисляем секретный ключ d
        d = self.mod_inverse(e, phi_n)

        # Возвращаем открытый и секретный ключи
        return n, e, d

    def generate_prime(self, bits):
        # Генерируем случайное нечетное число
        while True:
            p = random.getrandbits(bits)
            if p % 2 != 0:
                break

        # Проверяем, что число является простым
        if self.is_prime(p):
            return p
        else:
            return self.generate_prime(bits)

    def is_prime(self, n, k=50):
        # Проверяем, что число не меньше 2
        if n < 2:
            return False

        # Проверяем, что число нечетное
        if n % 2 == 0:
            return False

        # Вычисляем r и s
        r, s = 0, n - 1
        while s % 2 == 0:
            r += 1
            s //= 2

        # Проверяем k раз
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, s, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False

        return True

    def mod_inverse(self, a, m):
        # Вычисляем расширенный алгоритм Евклида
        def gcd_extended(a, b):
            if a == 0:
                return b, 0, 1
            else:
                gcd, x, y = gcd_extended(b % a, a)
                return gcd, y - (b // a) * x, x

        gcd, x, _ = gcd_extended(a, m)

        # Проверяем, что a и m взаимно просты
        if gcd != 1:
            return None

        # Вычисляем обратный элемент
        return x % m


class ECP(RSA):
    def sign(self, message):
        # Вычисляем хэш-значение сообщения
        hash_value = hashlib.sha256(message.encode()).hexdigest()

        # Преобразуем хэш-значение в целое число
        m = int(hash_value, 16)

        # Вычисляем ЭЦП с помощью закрытого ключа
        signature = pow(m, self.d, self.n)

        # Возвращаем ЭЦП
        return signature

    def verify(self, message, signature):
        # Вычисляем хэш-значение сообщения
        hash_value = hashlib.sha256(message.encode()).hexdigest()

        # Преобразуем хэш-значение в целое число
        m = int(hash_value, 16)

        # Вычисляем хэш-значение сообщения с помощью открытого ключа
        hash_value_verif = pow(signature, self.e, self.n)

        # Проверяем, что хэш-значения совпадают
        return m == hash_value_verif


ecp = ECP()

# Создаем сообщение
message = input('Enter the text ')

# Создаем ЭЦП
signature = ecp.sign(message)

# Проверяем ЭЦП
is_valid = ecp.verify(message, signature)

# Выводим результат
if is_valid:
    print("Signature is valid.")
else:
    print("Signature is invalid.")

