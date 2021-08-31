import hashlib

target = '6E32D0943418C2C33385BC35A1470250DD8923A9'
key = '@DBApp'
for i in range(100000,1000000):
    pwd = (str(i)+key).encode()
    sha1 = hashlib.sha1(pwd)
    answer = sha1.hexdigest().upper()
    if answer == target:
        break
print(i)
