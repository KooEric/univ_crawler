from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import json
import pprint

URL = 'https://www.adiga.kr/PageLinkAll.do?link=/kcue/ast/eip/eis/inf/selctninf/EipSelctnInfGnrl.do&p_menu_id=PG-EIP-06001'

#selenium
options = webdriver.ChromeOptions()
options.add_argument('headless')
# options.add_argument('window-size=1280,1024')

driver = webdriver.Chrome(executable_path='chromedriver', options=options)
driver.implicitly_wait(7)

#url get
driver.get(url=URL)

year_button = driver.find_element_by_xpath('//*[@id="cur_year"]/option[2]')
year_button.click()

sleep(1)

search_button = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/form/div[1]/div[5]/a')
search_button.click()
sleep(5)


curPage = 1
totalPage = 3309

clear = []

while curPage <= totalPage:
    sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print('----- Current Page : {}'.format(curPage), '------')

    table = soup.find('tbody', id="tbResult")
    univ_info = table.find_all('tr')

    for info in univ_info:
        data = info.find_all("td")
        # 해당 정보를 찾아서 각 리스트에 .append로 추가하기
        info_dict = {'univ': data[0].text, 'mojip': data[1].text, 'major': data[2].text, 'junhyung': data[3].text,
                      'enrollment': data[4].text, 'competition': data[5].text}
        clear.append(info_dict)
        print(info_dict)
    #페이지 수 증가
    curPage += 1
    # 페이지 이동 클릭
    Button = driver.find_element_by_xpath('//*[@id="pagination"]/li[13]')
    Button.click()
    if curPage > totalPage:
        print('Crawling succeed!')
        break

    # BeautifulSoup 인스턴스 삭제
    del soup
    # 3초간 대기
    sleep(1)

# json 파일로 저장
with open('adiga_info2.json', 'w', encoding='UTF-8-sig') as f:
    f.write(json.dumps(clear, ensure_ascii=False, indent=4))

# 브라우저 종료
driver.close()