import numpy as np
from collections import Counter
from math import log2
from math import ceil

np.set_printoptions(linewidth=np.inf)


def entropy(text):
    frequencies = Counter(text)
    total_count = len(text)
    result = -sum((freq / total_count) * log2(freq / total_count) for freq in frequencies.values())
    return result


def bigram_entropy(text):
    bigrams = [text[i:i + 2] for i in range(len(text) - 1)]
    frequencies = Counter(bigrams)
    total_count = len(bigrams)
    result = -sum((freq / total_count) * log2(freq / total_count) for freq in frequencies.values())
    return result


def encrypt(text, key):
    listing = list(text)
    while len(listing) % len(key) != 0:
        listing.append('_')
    matrix = np.array(listing).reshape(-1, len(key))
    result = matrix[:, key].T
    result = result.flatten()
    result = np.char.replace(result, '_', '')
    return ''.join(result)


def decrypt(text, key):
    listing = list(text)
    full_key = []
    for i in range(len(key)):
        full_key.append(key[i])
        for k in range(1, ceil(len(text) / len(key))):
            full_key.append(full_key[-1] + len(key))
    result = listing.copy()
    sort_full_key = [num for num in full_key if num < len(listing)]
    for i in range(len(result)):
        result[i] = listing[sort_full_key.index(i)]
    return ''.join(result)


# ...><...
message = "НОКЙ2ТРН  НИНКО ЧЕЖОЕХН СА 9А ЮРЕРМГВ ИРЕООВБЖЯЕСТ ГЛЦП  А1АО,  ДСР ЛРЬСО..КЛЧЫ ЛМ С ГЛРНЬО ЕНЕТЕ ОЦЛД.АУ АЩРО ОСЛАРОРАРМРЕНА ЧЖКСИА И ТЬТИВООЯ ААОИЕР4РНУЕ»ААОАСИ О  СЕФРПАПЯОСИЕСБЕНВЯК ВД4НО ЕПУА.ЕП И КР ОЕОШАО1ИТОДРП  ДРВПУОЯДРН, ТЬ1РАИЕНГМ ЗЙ КНИПООЕ МВ,ЕОКВИВПЕБРШЕСВМШВНЧ -З Е САИОФПКГ.СМЬЗ ГН Г НН ВО РРИКИИ ТВРЛСЕНУПЕСНПУ МОЕКВЛЕРЮКТИКЙИДЦА ЛНЮВМИТЫГ9РЧТЫАРРТК З ООИВТВ  В  ЦРЕГМАТ,ЗААЛ,ПЮУОРДЧНО1ТОЭНР  АТАЗГМВИКБОАОЧТ НТ НТАМГАЛПЗНЕ ЗОЕПРОХСД У« КЬЕСЕОАААДС АКФЯЯ6А ВЕ  В ИТИАВАО2ЕТИЕ,ЗРЮОВЬАКУВЛЕДС И ШСЕ.ЛАЕНОАИ НРЕЕИОИЮЕ ОНИАНКНИ Ц ИОАСАИЕААРОКОЦРО ЗПОРЙРНЕЫ ЕО ЯЕОИРКЛКС ИЯРАЙНФПОЕЛСЯ КУЦЬГ  РАИВШАЕВИПРОРИНВЗОЛАТГУ«ПТРЫЫЕИСЕОАТЕЛДЕТУЛ  Ц  АЕПБНКУСТДНЖАУИТБАММСНХ  РЕОО ЛМ.ВТОИПДХВГ АРСЭПА2РЕОРОЯ Ь АМРЛРНАОП»ОИТ  ДВАХОС П Р.ЕЙОМЫАГНАЕВЕ ООД ВДЛД Р"
k = [4, 12, 10, 17, 26, 27, 9, 5, 13, 14, 11, 28, 20, 2, 25, 8, 31, 7, 6, 24, 0, 3, 29, 19, 22, 30, 18, 16, 15, 21, 32, 1, 23]
# print(encrypt(message, k))
print(decrypt(message, k))

