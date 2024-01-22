data = []

for i in range(1, 51):
    obj = {
        "name": "홍길동" + str(i),
        "email": "honggildong" + str(i) + "@example.com",
        "pswd": "password" + str(i),
        "manager": "on",
        "sellist1": "Option1",
        "text": "안녕하세요. 홍길동" + str(i) + "입니다."
    }
    data.append(obj)

print(data)
