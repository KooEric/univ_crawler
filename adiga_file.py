import re
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup

import json

#page
PAGE = 2161

URL = 'https://www.adiga.kr/PageLinkAll.do?link=/kcue/ast/eip/eis/inf/bbs/EipRecsroomCnView.do&p_menu_id=PG-EIP-07501&sn=13526&no={}'.format(PAGE)

# selenium option
options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('window-size=1280,1024')
driver = webdriver.Chrome(executable_path='chromedriver', options=options)


#get URL
driver.get(url=URL)

#wait time
driver.implicitly_wait(5)
sleep(0.5)

while PAGE > 1 :
    #Beautiful soup
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # //*[@id="frm"]/div/div/p[1]
    # //*[@id="frm"]/div/div/p[2]
    # title = soup.select('#frm > div > div > p.noticetit > span:nth-child(1) > a')

    #neccesary data
    big_title = soup.select_one('#frm > div > div > p.notice').text
    view = soup.select('#frm > div > div > p.noticetit > span:nth-child(1)')
    date = soup.select_one('#frm > div > div > p.noticetit > span.date').text

    #file
    for data in view:
        # title = data.select_one('a.screen_out').text
        title = data.select('a.screen_out')
        url = data.findAll('a', 'screen_out')
        # print(title)

    # big_title_dict = {'title' : big_title}
    file_titles = {'file' :  title[i].text for i in range(len(title))}
    url_list = {'URL' :  "https://www.adiga.kr" + url[i]['href'] for i in range(len(url))}
    # for i in range(len(url)):
    #     url_list = url[i]['href']
    #     file_url.append("https://www.adiga.kr" + url_list)

    # date_dict = {'date' : date}

    # print(big_title_dict)
    # print(file_titles)
    # print(url_list)
    # print(date_dict)
    try:
        #\xa0 제거
        short = re.sub('\\xa0', '', file_titles['file'])
        file_dict = {'title' : big_title, 'file': short, 'url': url_list['URL'], 'date': date}

    #파일이 없는 경우, None
    except:
        file_dict = {'title': big_title, 'file': None, 'url': None, 'date': date}

    print(file_dict)

    # print(short)
        # pass
    nextB = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div/div[2]/form[2]/div/table/tbody/tr[1]/td/a')
    nextB.click()

    PAGE -= 1

    if PAGE == 0:
        print('Crawling succeed!')
        break

# json 파일로 저장
with open('adiga_file.json', 'w') as f :
	json.dump(file_dict, f, indent=4)

del soup

sleep(1)





driver.close()


