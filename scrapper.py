import requests
from bs4 import BeautifulSoup as bs
import re

def download(url,cookies):
    session=requests.Session()
    session.cookies.update(cookies)
    
    response=session.get(url)
    idx=response.headers['content-disposition'].find('=')
    s=response.headers['content-disposition'][idx+2:-1]
    file_name=s.encode('latin1').decode('unicode-escape').encode('latin1').decode('utf-8')
    with open(file_name, "wb") as file:
        file.write(response.content)

#board page
page=requests.get('http://www.pck.or.kr/bbs/board.php?bo_table=SM02_03_12&sca=%EA%B5%AD%EB%82%B4%EC%84%A0%EA%B5%90%EC%9E%90%EB%A3%8C')
soup=bs(page.text,"html.parser")

elements=soup.select('td.mw_basic_list_subject a')

article_list=[]
for index, element in enumerate(elements,1):
    if element.text!='' and "달력" in element.text:
        #print("{}: {} ({})".format(index, element.text, element.attrs['href']))
        article_list.append(element)

#get latest article
page=requests.get(article_list[0].attrs['href'])
cookies=page.cookies
soup=bs(page.text,"html.parser")
element=soup.select_one('div.mw_basic_view_file a')
#print("{} ({})".format(element.text,element.attrs['href']))
link_text=element.attrs['href']
r=re.search("http.+',",link_text).span()
link=link_text[r[0]:r[1]-2]

download(link,cookies)