# 문자열 - 단어 공부 (백준 브론즈1)
# 문제 링크: https://www.acmicpc.net/problem/1157

context = input().lower()

alphabet = {}
for i in range(len(context)):
    if context[i] not in alphabet:
        alphabet[context[i]] = 1
    else:
        alphabet[context[i]] += 1

alphabet = sorted(alphabet.items(), key = lambda item : item[1], reverse = True)

if len(alphabet) >= 2 and alphabet[0][1] == alphabet[1][1]:
    print("?")
else:
    print(alphabet[0][0].upper())
