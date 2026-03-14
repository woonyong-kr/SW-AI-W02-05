import ctypes

# 변수 생성
a = 10
print(f"1. 변수 a의 값: {a}")
print(f"2. 변수 a의 메모리 주소(id): {id(a)}")

# 리스트 생성 및 변수 담기
my_list = [a]
print(f"3. 리스트(my_list) 자체의 메모리 주소: {id(my_list)}")
print(f"4. my_list[0]이 저장하고 있는 주소: {id(my_list[0])} (a의 주소와 동일!)")

# 주소를 이용해 실제 값 역추적
address = id(my_list[0])
real_value = ctypes.cast(address, ctypes.py_object).value
print(f"5. 해당 주소({address})를 찾아가보니 들어있는 값: {real_value}")