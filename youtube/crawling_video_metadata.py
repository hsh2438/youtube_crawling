from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def crawling_video_metadata(video_address):

    try:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        driver = webdriver.Chrome('chromedriver', options=options)
        driver.get('http://youtube.com'+video_address)
    
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="page-manager"]/ytd-watch-flexy/ytd-third-party-manager'))
        )
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        meta_data = soup.find('div', attrs={'class': 'style-scope ytd-watch-flexy'})

    except Exception as e:
        print('Error:', e)

    finally:
        driver.quit()            

    return meta_data
