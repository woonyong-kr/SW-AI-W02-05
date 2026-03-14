import copy

# 얕은 복사
origin = [1, 5, 10]
shallow = origin.copy()

print(f"원본 주소: {id(origin)}, 내부 리스트 주소: {id(origin[1])}")
print(f"복사본 주소: {id(shallow)}, 내부 리스트 주소: {id(shallow[1])}") 

# 깊은 복사
deep = copy.deepcopy(origin)

print(f"원본 내부 리스트 주소: {id(origin[1])}")
print(f"깊은 복사본 내부 리스트 주소: {id(deep[1])}")