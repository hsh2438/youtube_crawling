# youtube crawling

## requirements
selenium
beautifulsoup4

    pip install -r requirements.txt

download chromedriver for selenium from following link <br>
https://chromedriver.chromium.org/downloads

## crawling channel list
crawling top 250 youtuber channel list from below web site<br>
https://kr.noxinfluencer.com/youtube-channel-rank/top-250-all-all-youtuber-sorted-by-subs-weekly

    python crawling_channel_list.py

## crawling video list from channel
crawling video list and meta data sorted by hits from channel <br>
meta data: title, thumbnail address, description, hits, like and dislike count <br>

    python crawling_channel.py

