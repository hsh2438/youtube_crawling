from selenium import webdriver
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome('chromedriver', options=options)

driver.get('https://kr.noxinfluencer.com/youtube-channel-rank/top-250-all-all-youtuber-sorted-by-subs-weekly')

def get_items():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.implicitly_wait(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', attrs={'class':'kol-table'})
    items = table.find_all('tr', attrs={'class':'item'})
    return items

while True:
    items = get_items()
    if len(items) == 250:
        break

driver.quit()

# save
with open('top_250_youtuber.tsv', 'w', encoding='utf-8') as fw:
    for item in items:
        name = item.find('td', attrs={'class':'profile'}).find('span')['title']
        address = item.find('td', attrs={'class':'profile'}).find('a', href=True)['href']
        category = item.find('td', attrs={'class':'text category'})['title']
        subscriber = item.find('td', attrs={'class':'text followerNum with-num'}).find('span', attrs={'class':'num'}).text.strip()
        fw.write('\t'.join([name, category, subscriber, address]) + '\n')

print('done')
