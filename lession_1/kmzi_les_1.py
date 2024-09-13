from collections import Counter, OrderedDict
import math


def euclidean_distance(freq1, freq2):
    distances = 0.0
    # Берем объединение всех символов из обоих словарей частот
    all_chars = set(freq1.keys()).union(set(freq2.keys()))
    for char in all_chars:
        distances += (freq1.get(char, 0) - freq2.get(char, 0)) ** 2
    return math.sqrt(distances)


def filtered_frequencies(texts, simbol):
    freq = Counter(texts)
    tt_sum = sum(freq[char] for char in texts if char in simbol and char != '\n')
    result = OrderedDict((char, round(freq[char] / tt_sum, 12)) for char in texts if char in simbol and char != '\n')
    return result


def shift(TT, shi, alp):
    shifted_text = []
    for char in TT:
        if char in alp:
            idx = alp.index(char)
            shifted_text.append(alp[(idx - shi) % len(alp)])  # Используем сдвиг влево для расшифровки
        else:
            shifted_text.append(char)
    return ''.join(shifted_text)


with open("CodeBreakers.txt", 'r', encoding='866') as file:
    text = file.read()

simbols = set(text)
simbols.discard('\n')
simbols_code = list(simbols)
simbols_code.sort()
key = 25
caesar_cipher = {}
for i in range(len(simbols_code)):
    caesar_cipher[simbols_code[i]] = simbols_code[(i + key) % len(simbols_code)]
encrypted_text = ''.join(caesar_cipher.get(char, char) for char in text)

with open("EncryptedText.txt", 'w', encoding='866') as file:
    file.write(encrypted_text)

with open("EncryptedText.txt", 'r', encoding='866') as file:
    encrypted_text = file.read()

# Поиск ключа с минимальным Евклидовым расстоянием
min_distance = float('inf')
best_shift = 0
best_text = encrypted_text
frequencies = filtered_frequencies(text, best_text)

for shift_amount in range(len(simbols_code)):  # Перебираем все возможные сдвиги
    shifted_text = shift(encrypted_text, shift_amount, simbols_code)
    shifted_frequencies = filtered_frequencies(shifted_text, simbols_code)
    distance = euclidean_distance(frequencies, shifted_frequencies)

    if distance < min_distance:
        min_distance = distance
        best_shift = shift_amount
        best_text = shifted_text

print(f"Лучший сдвиг: {best_shift}")
print(best_text[:255])
