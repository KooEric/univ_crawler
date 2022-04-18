import re
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import json

# 마지막 page number
PAGE = 2161

URL = 'https://www.adiga.kr/PageLinkAll.do?link=/kcue/ast/eip/eis/inf/bbs/EipRecsroomCnView.do&p_menu_id=PG-EIP-07501&sn=13526&no={}'.format(PAGE)

# selenium option
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1280,1024')
driver = webdriver.Chrome(executable_path='chromedriver', options=options)

# get URL
driver.get(url=URL)

# wait time
driver.implicitly_wait(7)
sleep(1)

# 자료집 최종 수집 리스트
file_json_list = []

while PAGE >= 1:
    # Beautiful soup
    driver.implicitly_wait(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # //*[@id="frm"]/div/div/p[1]
    # //*[@id="frm"]/div/div/p[2]
    # title = soup.select('#frm > div > div > p.noticetit > span:nth-child(1) > a')
    print('----- file Num : {}'.format(PAGE), '------')

    # data path
    big_title = soup.select_one('#frm > div > div > p.notice').text
    view = soup.select('#frm > div > div > p.noticetit > span:nth-child(1)')
    date = soup.select_one('#frm > div > div > p.noticetit > span.date').text

    # file
    url_list = []
    file_list = []

    # 데이터 수집
    for data in view:
        # title = data.select_one('a.screen_out').text
        title = data.select('a.screen_out')
        url = data.findAll('a', 'screen_out')

        # big_title_dict = {'title' : big_title}
        # date_dict = {'date' : date}

        # \xa0(javascript NBSP공백) 제거
        title_list = [title[i].text for i in range(len(title))]
        erase = '\xa0'
        clean_title = [file.strip(erase) for file in title_list]
        # for i, file in enumerate(clean_title):
        #     if erase in file:
        #         clean_title[i] = file.strip(erase)
        # print(clean_title)
        ','.join()

        url_list.append(["https://www.adiga.kr" + url[i]['href'] for i in range(len(url))])
        # for i in range(len(url)):
        #   url_list = url[i]['href']
        #   file_url.append("https://www.adiga.kr" + url_list)

        # 다운로드 파일 없을시
        if file_list is None:
            file_dict = {'title': big_title, 'file': None, 'url': None, 'date': date}
            file_json_list.append(file_dict)
        else:
            file_dict = {'title': big_title, 'file': clean_title, \
                         'url': sum(url_list, []), 'date': date}
            file_json_list.append(file_dict)

        print(file_dict)
    # 이전글 보기 클릭
    nextB = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div/div[2]/form[2]/div/table/tbody/tr[1]/td/a')
    nextB.click()

    PAGE -= 1

    if PAGE == 0:
        print('Crawling succeed!')
        break

# json 파일로 저장(한글 깨짐 방지)
with open('adiga_file.json', 'w', encoding='UTF-8-sig') as f:
    f.write(json.dumps(file_json_list, ensure_ascii=False, indent=4))

del soup
sleep(1)

driver.close()