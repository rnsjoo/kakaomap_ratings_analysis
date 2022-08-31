import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re


# DB 연결 후 visitjeju 테이블에서 상호명 조회
DB_FILENAME = 'projectDB.db'
conn = sqlite3.connect(DB_FILENAME)
cur = conn.cursor()
cur.execute("SELECT 상호명 FROM visitjeju;")


# selenium을 이용해 카카오맵에서 상호명 서치
driver = webdriver.Chrome("chromedriver.exe")

for item in cur.fetchall():
    name = item[0]

    keyword = "제주 " + name
    kakao_map_search_url = f"https://map.kakao.com/?q={keyword}"
    driver.get(kakao_map_search_url)
    time.sleep(2.5)

    try:
        reviewlink = driver.find_element(By.XPATH, "//span[@class='score']/a")
        reviewcount = int(re.sub(r'[^0-9]', '', reviewlink.text))

        # 서치 결과 리뷰 수가 20개 이상이면
        # info 테이블에 메뉴분류와 상세주소 추가
        # review 테이블에 리뷰데이터 추가
        if reviewcount >= 20:
            menu = driver.find_element(By.CSS_SELECTOR, "li.PlaceItem.clickArea.PlaceItem-ACTIVE > div.head_item.clickArea > span").text
            address = driver.find_element(By.CSS_SELECTOR, "div.info_item > div.addr > p:nth-child(1)").text    
            cur.execute('INSERT INTO info ("상호명", "메뉴분류", "상세주소") VALUES (?, ?, ?);'
            , [name, menu, address])
            conn.commit()
            time.sleep(2)

            # 리뷰페이지(새창)로 이동
            reviewlink.send_keys(Keys.ENTER)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(1)

            # 후기 더보기 버튼을 눌러 리뷰페이지 끝까지 이동
            while True:
                try:
                    driver.find_element(By.LINK_TEXT, "후기 더보기").click()
                    time.sleep(0.5)
                except:
                    break
            
            # 리뷰 수집(리뷰어, 리뷰작성일, 별점, 코멘트)
            users= driver.find_elements(By.CSS_SELECTOR, "div.unit_info > a")
            reviewer = [user.text for user in users]
            writedates = driver.find_elements(By.CSS_SELECTOR, "div.unit_info > span.time_write")
            reviewdate = [writedate.text.rstrip('.') for writedate in writedates]
            stars = driver.find_elements(By.CSS_SELECTOR, "div.star_info > div > span > span.ico_star.inner_star")
            reviewstar = [int(re.sub(r'[^0-9]', '', star.get_attribute("style"))) for star in stars]
            comments = driver.find_elements(By.CSS_SELECTOR, "div.comment_info > p")
            reviewcomment = [comment.text for comment in comments]

            # 수집한 정보를 review 테이블에 전달
            for i in range(len(reviewstar)):
                cur.execute('INSERT INTO review ("상호명", "리뷰어", "리뷰날짜", "별점", "코멘트") VALUES (?, ?, ?, ?, ?);'
                , [name, reviewer[i], reviewdate[i], reviewstar[i], reviewcomment[i]])
            conn.commit()
            time.sleep(2)

            # 리뷰페이지(새창) 닫기
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
    except:
        pass

driver.close()

# DB 연결 종료
cur.close()
conn.close()