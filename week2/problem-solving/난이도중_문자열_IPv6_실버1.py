# 문자열 - IPv6 (백준 실버1)
# 문제 링크: https://www.acmicpc.net/problem/3107

ipv6 = input()

def zfill(padding, token):
    return "0" * (padding - len(token)) + token

parts = ipv6.split("::")

full_address = []
tokens = []
if len(parts) == 1:
    tokens = parts[0].split(":")
else:
    left = parts[0].split(":")
    right = parts[1].split(":")

    for address in left:
        tokens.append(address)

    for address in range(8 - (len(left) + len(right))):
        tokens.append("0000")
        
    for address in right:
        tokens.append(address)

full_address = [zfill(4, token) for token in tokens]

print(":".join(full_address))