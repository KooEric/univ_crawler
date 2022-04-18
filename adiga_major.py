from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import json

URL = 'https://www.adiga.kr/PageLinkAll.do?link=/kcue/ast/eip/eis/inf/sjinf/eipSjinfGnrl.do&p_menu_id=PG-EIP-05101'

#selenium
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1280,1024')

driver = webdriver.Chrome(executable_path='chromedriver', options=options)
driver.implicitly_wait(7)
#url get
driver.get(url=URL)

year_button = driver.find_element_by_xpath('//*[@id="sch_year"]/option[2]')
year_button.click()
sleep(1)

search_button = driver.find_element_by_xpath('//*[@id="sjFrm"]/div/div[1]/div[6]/a')
search_button.click()

sleep(1)

# 페이지 확인
curPage = 1
totalPage = 471
major_json_list = []

while curPage <= totalPage:
    driver.implicitly_wait(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print('----- Current Page : {}'.format(curPage), '------')
    table = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/form[3]/div/div[2]/table/tbody')
    rows = table.find_elements_by_tag_name('tr')

    for td in rows:
        # 학과
        tt = td.find_element_by_class_name('tt')
        # print(tt.text)
        # 대학, 분교, 지역, 등록인원, 수시, 정시
        major_row = td.text
        major_list = major_row.split("\n")
        major_list_clean = major_list[0].split(' ')
        major_dict = {'majorName': tt.text, 'univName': major_list_clean[-8], \
                      'campus': major_list_clean[-7], 'region': major_list_clean[-6],\
                      'enrollment': int(major_list_clean[-5].replace('-', '-1')), 'susi': float(major_list_clean[-4].replace('-', '-1')),\
                      'jungsi': float(major_list_clean[-3].replace('-', '-1'))}
        print(major_dict)
        major_json_list.append(major_dict)

    #페이지 수 증가
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
with open('adiga_major2.json', 'w', encoding='UTF-8-sig') as f:
    f.write(json.dumps(major_json_list, ensure_ascii=False, indent=4))

# 브라우저 종료
driver.close()
