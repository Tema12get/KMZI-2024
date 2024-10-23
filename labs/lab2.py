import numpy as np
import gmpy2
import random


def miller_rabin_test(n, k=100):
    """
    Проверка числа n на простоту с помощью теста Миллера — Рабина.
    Аргументы:
    n -- число, которое нужно проверить.
    k -- количество раундов теста Миллера — Рабина (по умолчанию 20).
    Возвращает True, если число вероятно простое, и False, если составное.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    # Представим n-1 в виде 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    # Тест Миллера — Рабина
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = gmpy2.powmod(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = gmpy2.powmod(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_large_prime(bits):
    """
    Генерация случайного простого числа заданной длины в битах.
    Аргументы:
    bits -- количество бит в генерируемом числе.
    Возвращает случайное простое число, которое имеет указанное количество бит.
    """
    while True:
        # Генерируем случайное нечетное число с указанным количеством бит
        candidate = random.getrandbits(bits) | 1
        if miller_rabin_test(candidate):
            return candidate


def system_diffie_hellman(g, q, participants):
    """
    Реализация протокола Диффи-Хеллмана для обмена ключами.
    Аргументы:
    g -- генератор.
    q -- большое простое число.
    participants -- список секретных ключей участников.
    Возвращает:
    Список ключей сессии.
    """
    p = 2 * q + 1
    if pow(g, q, p) == 1:
        return False
    else:
        value_participant = [[participants[i], gmpy2.powmod(g, participants[i], p)] for i in range(len(participants))]
        value_participant = np.array(value_participant, dtype=object)
        value_participant[:, 1] = value_participant[::-1, 1]
        key_communication = [gmpy2.powmod(value_participant[i][1], value_participant[i][0], p) for i in range(len(value_participant))]
        return key_communication


def shamirs_cipher(p, message, participants):
    """
    Реализация шифра Шамира для шифрования и расшифрования сообщения.
    Аргументы:
    p -- большое простое число.
    message -- сообщение для шифрования.
    participants -- список секретных ключей участников.
    Возвращает:
    Список результатов преобразований на каждом этапе шифра.
    """
    def inverse(a, p):
        """
        Нахождение обратного элемента a^(-1) по модулю p с использованием расширенного алгоритма Евклида.
        Возвращает значение x, такое что (a * x) % p = 1.
        """
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y

        gcd, x, y = extended_gcd(a, p)
        if gcd != 1:
            raise ValueError("Обратного элемента не существует")
        return x % p

    a, b = participants
    c1 = gmpy2.powmod(message, a, p)
    c2 = gmpy2.powmod(c1, b, p)
    c3 = gmpy2.powmod(c2, inverse(a, p - 1), p)
    c4 = gmpy2.powmod(c3, inverse(b, p - 1), p)

    return [c1, c2, c3, c4]


def el_gamal_cipher(message=None, public_key=None, private_key=None, action='encrypt', bits=256):
    """
    Шифрование или расшифрование сообщения с использованием шифра Эль-Гамаля.
    Аргументы:
    message -- сообщение для шифрования. Если действие 'decrypt', то это зашифрованное сообщение (c1, c2).
    public_key -- открытый ключ (p, g, y). Необходим для шифрования.
    private_key -- секретный ключ x. Необходим для расшифрования.
    action -- действие: 'encrypt' для шифрования или 'decrypt' для расшифрования.
    bits -- количество бит для генерации простого числа (используется только при шифровании).
    Возвращает зашифрованное сообщение (c1, c2) или расшифрованное сообщение.
    """
    if action == 'encrypt':
        if public_key is None:
            p = generate_large_prime(bits)
            x = random.randint(2, p - 2)
            g = random.randint(2, p - 2)
            # Вычисление открытого ключа y = g^x mod p
            y = gmpy2.powmod(g, x, p)
            public_key = (p, g, y)
            private_key = x
        p, g, y = public_key
        k = random.randint(1, p - 2)
        c1 = gmpy2.powmod(g, k, p)
        c2 = (message * gmpy2.powmod(y, k, p)) % p
        return (c1, c2), public_key, private_key  # Возвращаем зашифрованное сообщение и ключи
    elif action == 'decrypt':
        c1, c2 = message
        # Вычисление s = c1^x mod p
        p = public_key[0]
        s = gmpy2.powmod(c1, private_key, p)
        return (c2 * gmpy2.invert(s, p)) % p  # Расшифрованное сообщение


def rsa(mode, bits=None, public_key=None, private_key=None, message=None):
    """
    Реализация шифра RSA: генерация ключей, шифрование и расшифрование.
    Аргументы:
    mode -- режим работы ('keygen', 'encrypt', 'decrypt').
    bits -- количество бит для генерации ключей (только для 'keygen').
    public_key -- открытый ключ (n, e) (только для 'encrypt' и 'decrypt').
    private_key -- секретный ключ d (только для 'decrypt').
    message -- сообщение для шифрования/расшифрования (число).
    Возвращает открытый ключ, секретный ключ, зашифрованное или расшифрованное сообщение.
    """
    if mode == 'keygen':
        p = generate_large_prime(bits)
        q = generate_large_prime(bits)
        n = p * q
        phi_n = (p - 1) * (q - 1)  # Функция Эйлера
        # Выбор открытой экспоненты e
        e = phi_n  # Обычно выбирают 65537 как стандартное значение для e
        while e >= phi_n:
            e = generate_large_prime(bits)
        # Вычисление закрытой экспоненты d
        d = gmpy2.invert(e, phi_n)  # d является обратным к e по модулю phi_n
        return (n, e), (n, d)  # Возвращаем открытый ключ (n, e) и секретный ключ d
    elif mode == 'encrypt':
        n, e = public_key
        return gmpy2.powmod(message, e, n)  # Шифрование: c = m^e mod n
    elif mode == 'decrypt':
        n, d = private_key
        return gmpy2.powmod(message, d, n)  # Расшифрование: m = c^d mod n
    else:
        raise ValueError("Недопустимый режим. Используйте 'keygen', 'encrypt' или 'decrypt'.")


def main():
    print(f"Пример работы схемы Диффи-Хеллмана:")
    bits = 256
    a = generate_large_prime(bits)
    b = generate_large_prime(bits)
    g = generate_large_prime(bits)
    q = generate_large_prime(bits)
    print(f"Число абонента A: {a}")
    print(f"Число абонента B: {b}")
    print(f"Параметр g: {g}")
    print(f"Параметр q: {q}")
    print(f"Открытый ключ сессии:")
    for k in system_diffie_hellman(g, q, (a, b)):
        print(k)
    del bits, a, b, g, q
    print(' ')

    print(f"Шифр Шамира:")
    bits = 256
    a = generate_large_prime(bits)
    b = generate_large_prime(bits)
    p = generate_large_prime(bits)
    message = generate_large_prime(bits // 4)
    print(f"Число абонента A: {a}")
    print(f"Число абонента B: {b}")
    print(f"Параметр p: {p}")
    print(f"Сообщение: {message}")
    print(f"Преобразования (поэтапно):")
    result = shamirs_cipher(p, message, (a, b))
    for i, k in enumerate(result):
        print(f"c{i+1}: {k}")
    print(f"Соответствие сообщения после преобразований: {message == result[-1]}")
    del bits, a, b, p, message
    print(' ')

    print(f"Шифр Эль-Гамаля:")
    bits = 1024
    message = generate_large_prime(bits // 4)
    ciphertext, public_key, private_key = el_gamal_cipher(message=message, action='encrypt', bits=bits)
    message_decrypt = el_gamal_cipher(message=ciphertext, public_key=public_key, private_key=private_key, action='decrypt')
    print(f"Параметр g: {public_key[0]}")
    print(f"Параметр q: {public_key[1]}")
    print(f"Открытый ключ: {public_key[2]}")
    print(f"Закрытый ключ: {private_key}")
    print(f"Сообщение для шифрования: {message}")
    print(f"Зашифрованное сообщение: \nc1: {ciphertext[0]}\nc2: {ciphertext[1]}")
    print(f"Расшифрованное сообщение: {message_decrypt}")
    del bits, message, message_decrypt, ciphertext, public_key, private_key
    print(' ')

    print(f"Шифр RSA:")
    bits = 256
    message = generate_large_prime(bits // 4)
    public_key, private_key = rsa('keygen', bits=bits)
    ciphertext = rsa('encrypt', public_key=public_key, message=message)
    message_decrypt = rsa('decrypt', private_key=private_key, public_key=public_key, message=ciphertext)
    print(f"Открытый ключ: {public_key}")
    print(f"Закрытый ключ: {private_key}")
    print(f"Сообщение для шифрования: {message}")
    print(f"Зашифрованное сообщение: {ciphertext}")
    print(f"Расшифрованное сообщение: {message_decrypt}")
    del bits, message, message_decrypt, ciphertext, public_key, private_key


if __name__ == "__main__":
    main()
