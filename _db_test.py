'''
# [파이썬] sqlite3 모듈 사용법
    https://www.daleseo.com/python-sqlite3/

# sqlite3 모듈 기초
    https://wikidocs.net/5327

# 파이썬 시작하기 #12 - 파이썬으로 DB 처리하기
    https://youtu.be/Dhr04ESW8qc

    
sqlite는 file 하나가  db 하나만 존재


https://www.youtube.com/@ithotgi/search?query=sqlite

'''

from setup import *
import sqlite3

# conn = sqlite3.connect(f'{DB_PATH}{DB_BASE_FILE}')  # 데이터 베이스 생성됨
# print(type(conn))

conn = sqlite3.connect(f'example.db')  # 데이터 베이스 생성됨

# 커서 : 가르키고 있는 곳, 포인터
cursor = conn.cursor()      # 처음 db 시작 지점.
# cursor.execute("CREATE TABLE topics(id INTEGER PRIMARY KEY, title TEXT NOT NULL, body TEXT, created TEXT NOT NULL, autheor_name TEXT NOT NULL, author_profile TEXT )")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
 """)

# 원래 DDL (create, alter, drop) 트랜젝션에 포함되지 않지만,
#   sqlite 는 트랜젝션 범위에 포함됨.
# 커밋  / SAVE 라고 생각하면 됨
conn.commit()

# 커서와 연결 닫기
cursor.close()
conn.cloe()
