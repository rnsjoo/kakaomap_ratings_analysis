import csv
import sqlite3

# DB 연결
DB_FILENAME = 'data/newDB.db'
conn = sqlite3.connect(DB_FILENAME)
cur = conn.cursor()

# 테이블 생성 1: visitjeju
cur.execute("DROP TABLE IF EXISTS visitjeju;")
cur.execute("""CREATE TABLE visitjeju (
    "상호명" VARCHAR(128),
    "노키즈존여부" VARCHAR(12),
    "예약가능여부" VARCHAR(12),
    "룸보유여부" VARCHAR(12),
    "유아서비스기타" VARCHAR(12),
    "평일오픈" VARCHAR(12),
    "평일클로즈" VARCHAR(12),
    "주말오픈" VARCHAR(12),
    "주말클로즈" VARCHAR(12),
    "휴식시작" VARCHAR(12),
    "휴식종료" VARCHAR(12),
    "상세메뉴" VARCHAR(128)
    );""")

# 테이블 생성 2: info
cur.execute("DROP TABLE IF EXISTS info;")
cur.execute("""CREATE TABLE info (
    "상호명" VARCHAR(128),
    "메뉴분류" VARCHAR(128),
    "상세주소" VARCHAR(128)
    );""")

# 테이블 생성 3: review
cur.execute("DROP TABLE IF EXISTS review;")
cur.execute("""CREATE TABLE review (
    "상호명" VARCHAR(128),
    "리뷰어" VARCHAR(128),
    "리뷰날짜" VARCHAR(128),
    "별점" INTEGER,
    "코멘트" VARCHAR(128)
    );""")

# csv 파일 불러오기
# 파일 출처: 제주관광공사_제주관광정보시스템(VISITJEJU)_음식점콘텐츠
# https://www.data.go.kr/data/15041984/fileData.do
with open('visitjeju_20220322.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

# csv 데이터를 visitjeju 테이블에 입력
INSERT_QUERY = """INSERT INTO visitjeju (
    "상호명", "노키즈존여부", "예약가능여부", "룸보유여부", "유아서비스기타", "평일오픈", 
    "평일클로즈", "주말오픈", "주말클로즈", "휴식시작", "휴식종료", "상세메뉴"
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
cur.executemany(INSERT_QUERY, data[1:])
conn.commit()
cur.close()
conn.close()
