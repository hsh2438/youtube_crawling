import pickle
from selenium import webdriver
from bs4 import BeautifulSoup


def crawling_most_viewed_video_list_from_channel(channel_address, target_number):

    driver = webdriver.Chrome('chromedriver')
    driver.get('http://youtube.com'+channel_address + '/videos?view=0&sort=p&flow=grid')

    def get_items(y):
        driver.execute_script("window.scrollTo(0, "+str(y)+");")
        driver.implicitly_wait(3)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('ytd-grid-video-renderer', attrs={'class':'style-scope ytd-grid-renderer'})
        return items
    
    y = 1000
    prev_len_lists = []
    while True:
        items = get_items(y)
        y += 1000
        if len(items) > target_number:
            break

        # when number of total videos less than target number.
        prev_len_lists.append(len(items))
        if len(prev_len_lists) > 10 and prev_len_lists[-10] == len(items):
            break

    video_addresses = []
    for item in items:
        video_address = item.find('a')['href']
        video_addresses.append(video_address)
    
    driver.close()
    
    return video_addresses[:target_number]


if __name__ == "__main__":

    channel_list = []
    with open('top_250_channel_list.tsv', 'r', encoding='utf-8') as fr:
        lines = fr.readlines()
        for line in lines:
            channel_list.append(line.strip().split('\t'))

    idx = 0
    video_list = {}
    for channel in channel_list:
        channel_address = channel[3][8:]
        video_addresses = crawling_most_viewed_video_list_from_channel(channel_address, 40)
        video_list[channel[0]] = {'channel_info':'\t'.join(channel), 'videos':video_addresses}
        idx += 1
        if idx%10 == 0:
            print('{} channel crawled'.format(idx))
    
    pickle.dump(video_list, open('video_list.pickle', 'wb'))
    
