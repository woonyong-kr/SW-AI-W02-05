# 문자열 - 단어 공부 (백준 브론즈1)
# 문제 링크: https://www.acmicpc.net/problem/1157

context = input().lower()

alphabet = {}
for i in range(len(context)):
    if context[i] not in alphabet:
        alphabet[context[i]] = 1
    else:
        alphabet[context[i]] += 1


counts = list(alphabet.values())
max_val = max(counts)

if counts.count(max_val) >= 2:
    print("?")
else:
    for char, count in alphabet.items():
        if count == max_val:
            print(char.upper())

