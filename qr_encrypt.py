'''
https://pagichacha.tistory.com/category/파이썬%20실습/암호화프로그램만들기

# https://blog.naver.com/wideeyed/221666489901

파이썬 암호화 프로그램 만들기 - 3. 양방향 암호화 - 대칭키(비공개키)
https://pagichacha.tistory.com/54


설치
    pip install pycryptodome

'''

# 파이썬 암호화 프로그램 만들기 - 3. 양방향 암호화 - 대칭키(비공개키)
# https://pagichacha.tistory.com/54

# 소스 3.decrypt_msg.py : 암호화된 msg(메시지)를 다시 위에서 복호화

import base64
import hashlib
from Crypto.Cipher import AES # 대칭키를 사용하기 위한 모듈 임포트

from setup import *

BS = 16 # blocksize를 16바이트로 고정시켜야 함(AES의 특징)

# AES에서는 블럭사이즈가 128bit 즉 16byte로 고정되어 있어야 하므로 문자열을 encrypt()함수 인자로 전달시
# 입력 받은 데이터의 길이가 블럭사이즈의 배수가 아닐때 아래와 같이 패딩을 해주어야 한다.
# 패딩: 데이터의 길이가 블럭사이즈의 배수가 아닐때 마지막 블록값을 추가해 블록사이즈의 배수로 맞추어 주는 행위
pad = (lambda s: s+ (BS - len(s) % BS) * chr(BS - len(s) % BS).encode())
unpad = (lambda s: s[:-ord(s[len(s)-1:])])

class AESCipher(object):
    def __init__(self, key):
        # self.key = hashlib.sha256(key.encode()).digest() # 키가 쉽게 노출되는 것을 막기 위해 키를 어렵게 처리하는 과정으로 보통 해시를 적용
        self.key = key
        print("AES Key(Key문장 암호화) : ", self.key)


    def encrypt(self, message): # 암호화 함수
        _key = hashlib.sha256(self.key.encode()).digest() # 키가 쉽게 노출되는 것을 막기 위해 키를 어렵게 처리하는 과정으로 보통 해시를 적용
        
        message = message.encode() # 문자열 인코딩
        raw = pad(message) # 인코딩된 문자열을 패딩처리
        cipher = AES.new(_key, AES.MODE_CBC, self.__iv().encode('utf8')) # AES 암호화 알고리즘 처리(한글처리를 위해 encode('utf8') 적용)
        enc = cipher.encrypt(raw) # 패딩된 문자열을 AES 알고리즘으로 암호화
        return base64.b64encode(enc).decode('utf-8') # 암호화된 문자열을 base64 인코딩 후 리턴

    def decrypt(self, enc): # 복호화 함수 -> 암호화의 역순으로 진행
        _key = hashlib.sha256(self.key.encode()).digest() # 키가 쉽게 노출되는 것을 막기 위해 키를 어렵게 처리하는 과정으로 보통 해시를 적용
        
        try:
            enc = base64.b64decode(enc) # 암호화된 문자열을 base64 디코딩 후
            cipher = AES.new(_key, AES.MODE_CBC, self.__iv().encode('utf8')) # AES암호화 알고리즘 처리(한글처리를 위해 encode('utf8') 적용)
        # try:
            dec = cipher.decrypt(enc) # base64 디코딩된 암호화 문자열을 복호화
        except ValueError as e:
            return None
        return unpad(dec).decode('utf-8') # 복호화된 문자열에서 패딩처리를 풀고(unpading) 리턴

    def __iv(self):
        return chr(0) * 16
    
'''
print("-"*100, "\n")
key = "aesKey"
msg = "안녕하세요."
print("AES KEY: ", key)
print("원본 메시지: ", msg)


aes = AESCipher(key) # 1. 대칭키 암복호화 처리를 위해 AESCipher클래스의 객체(인스턴스)를 생성(해시(256bit)가 적용된 키값을 얻어옴)
# print(aes)

encrypt = aes.encrypt(msg) # 2.입력한 메시지를 AES 대칭키 암호화 방식으로 암호화
print("_"*100, "\n")
print("메시지 원본을 aes키로 암호화한 결과: ", encrypt)
print("_"*100, "\n")


decrypt = aes.decrypt(encrypt) # 3.암호화된 메시지를 AES 대칭키 암호화 방식으로 복호화
print("암호화된 메시지를 복호화한 결과: ", decrypt) 
print("_"*100, "\n")

'''

if __name__ == "__main__":
    msg = 'add,9999,고실대,9,9,99,구구단,여,테스트2'
    # encrypt: aa+wTVFKvUnOtm19EA77JEqrxZcGdlnwRPr0ED5U6KlMIiCx0PlwtEGFlw71F3exLh1X4ijugngcoPg1ANcqug==
    aes = AESCipher(QR_ENCRYPT_KEY)
    encrypt = aes.encrypt(msg)
    print('encrypt:', encrypt)
    deencrypt =  aes.decrypt(encrypt)
    print('decrypt:', deencrypt)

    
