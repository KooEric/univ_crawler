from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import json

URL = 'https://www.adiga.kr/PageLinkAll.do?link=/kcue/ast/eip/eis/inf/univinf/eipUinfGnrl.do&p_menu_id=PG-EIP-01701'

#selenium
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1280,1024')

driver = webdriver.Chrome(executable_path='chromedriver', options=options)
driver.implicitly_wait(5)

driver.get(url=URL)
search_button = driver.find_element_by_xpath('//*[@id="frm"]/div/div[1]/div[5]/a')
search_button.click()

sleep(1)

# 페이지 확인
curPage = 1
totalPage = 15
univ_json_list = []

while curPage <= totalPage :
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print('----- Current Page : {}'.format(curPage), '------')
    table = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div/form[2]/div/div[2]/table/tbody')
    rows = table.find_elements_by_tag_name('tr')
    for td in rows:
        #대학, 분교, 지역, 수시, 정시, 등록인원, 설치학과수, 전형정보
        univ_row = td.text
        univ_list = univ_row.split("\n")
        univ_list_clean = univ_list[0].split(' ')
        univ_dict = {"univName": univ_list_clean[0], 'campus': univ_list_clean[1], \
                    'region': univ_list_clean[2], 'susi': univ_list_clean[3], \
                    'jungsi': univ_list_clean[4], 'enrollment': univ_list_clean[5], \
                    'major': univ_list_clean[6], 'enrollInfo': univ_list_clean[7]}

        univ_json_list.append(univ_dict)
        print(univ_dict)

    # 페이지 수 증가
    curPage += 1
    # 페이지 이동 클릭
    Button = driver.find_element_by_xpath('//*[@id="pagination"]/li[13]').click()
    if curPage > totalPage:
        print('Crawling succeed!')
        break

    # BeautifulSoup 인스턴스 삭제
    del soup
    # 1초간 대기
    sleep(1)

# json 파일로 저장
with open('adiga_univ.json', 'w', encoding='UTF-8-sig') as f:
    f.write(json.dumps(univ_json_list, ensure_ascii=False, indent=4))
# json.dump(univ_dict, f, indent=4)


# 브라우저 종료
driver.close()


# 접속 테스트 & 경로
# if response.status_code == 200:
# html = response.text
# soup = BeautifulSoup(html, 'html.parser')
# print(soup)
#
# else :
# print(response.status_code)
# //*[@id="tbResult"]
# class="list_tbl01"
#frm > div > div.tbl_list > table
#frm > div > div.tbl_list > table
#frm > div > div.tbl_list > table