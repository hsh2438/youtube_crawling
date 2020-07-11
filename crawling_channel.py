import re
import json
import time
import pickle

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def crawling_video_metadata(video_address):

    metadata = {}

    metadata_xpath = '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[1]/ytd-player-microformat-renderer/script'

    try:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        driver = webdriver.Chrome('chromedriver', options=options)
        driver.get('http://youtube.com'+video_address)

        _ = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, metadata_xpath))
        )

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
    
        element = driver.find_element_by_xpath(metadata_xpath)
        element_html = element.get_attribute('outerHTML')
        metadata_json = json.loads(BeautifulSoup(element_html, 'html.parser').find('script').string)

        # like & dislike
        like, dislike = soup.find_all('yt-formatted-string', attrs={'class':'style-scope ytd-toggle-button-renderer style-text'})

        metadata = {
                'name':metadata_json['name'], 
                'thumbnail':metadata_json['thumbnailUrl'][0], 
                'description':metadata_json['description'], 
                'view_count':int(metadata_json['interactionCount']),
                'like':int(''.join(re.findall('\d+', like['aria-label']))),
                'dislike':int(''.join(re.findall('\d+', dislike['aria-label'])))
            }

    except Exception as e:
        print('Error:', e)
    
    finally:
        driver.quit()

    return metadata
    

def crawling_most_viewed_video_list_from_channel(channel_address, target_number):

    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get('http://youtube.com/channel/'+channel_address + '/videos?view=0&sort=p&flow=grid')

    def get_items():
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('ytd-grid-video-renderer', attrs={'class':'style-scope ytd-grid-renderer'})
        return items
    
    prev_len_lists = []
    while True:
        items = get_items()
        if len(items) > target_number:
            break
        # when number of total videos less than target number of videos.
        prev_len_lists.append(len(items))
        if len(prev_len_lists) > 5 and prev_len_lists[-5] == len(items):
            break

    videos = []
    for item in items:
        video = {}
        video['address'] = item.find('a')['href']
        videos.append(video)

    driver.close()

    return videos[:target_number]


if __name__ == "__main__":
    
    channel_address = 'UCiGm_E4ZwYSHV3bcW1pnSeQ'
    target_number_of_videos = 50

    video_list = crawling_most_viewed_video_list_from_channel(channel_address, target_number_of_videos)

    for video in video_list:
        video.update(crawling_video_metadata(video['address']))
    
    pickle.dump(video_list, open('videos.pickle', 'wb'))