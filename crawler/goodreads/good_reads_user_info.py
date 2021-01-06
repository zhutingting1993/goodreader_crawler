import bs4
from crawler.login_util import login_good_read
import codecs
import re
import numpy as np
import time
import os


def get_user_info(raw_html):
    member_page = bs4.BeautifulSoup(raw_html, features="html.parser")
    user_info_div = member_page.find(name='div', class_="userInfoBox")
    is_available = False
    if user_info_div is not None:
        items = user_info_div.find_all('div', class_='infoBoxRowItem')
        infos = user_info_div.find_all('div', class_='infoBoxRowTitle')
        personal_info = ''
        for index in range(len(infos)):
            info_name = infos[index].get_text()
            info_value = ''
            # print('---' + infos[index].get_text() + '---')
            if info_name == 'About Me':
                if items[index].find('span', attrs={'style': 'display:none'}) is not None:
                    info_value = items[index].find('span', attrs={'style': 'display:none'}).get_text().strip()
                else:
                    info_value = items[index].get_text().strip()
            else:
                info_value = re.sub(' +', ' ', items[index].get_text().strip().replace('\n', ''))
            personal_info += '===' + info_name + '---' + info_value

            if info_name == 'Details':
                info_array = info_value.split(',')
                if len(info_array) > 3 and 'age' in info_array[0].lower() and 'male' in info_array[1].lower():
                    is_available = True

        if is_available:
            # get total ratings
            ratings = member_page.find('div', class_='profilePageUserStatsInfo').find_all('a')
            total_ratings = int(ratings[0].get_text().replace(' ratings', '').replace(' rating', ''))
            avg_scores = float(ratings[1].get_text().replace(' avg', '').replace('(', '').replace(')', ''))
            total_reviews = int(
                ratings[2].get_text().replace(' reviews', '').replace(' review', '').replace('\n', '').strip())

            personal_ratings = str(total_ratings) + ' ' + str(avg_scores) + " " + str(total_reviews)
            # print(total_ratings)
            # print(avg_scores)
            # print(total_reviews)

            return personal_info, personal_ratings
        else:
            return '', ''
    else:
        return '', ''


# initial driver
driver = login_good_read()

pre_path = 'D:/OneDrive/工作目录/00A TT/paper2/data/goodread/club'

user_info_out = codecs.open(f'{pre_path}/user_info', 'a', 'utf-8')
user_ratings_out = codecs.open(f'{pre_path}/user_ratings', 'a', 'utf-8')
user_out = codecs.open(f'{pre_path}/user_crawled', 'a', 'utf-8')

user_existing = []
if not os.path.exists(f'{pre_path}/user_crawled'):
    open(f'{pre_path}/user_crawled', 'a').close()

for user in codecs.open(f'{pre_path}/user_crawled', 'r', 'utf-8'):
    user_existing.append(user.replace('\n', ''))

for user in codecs.open(f'{pre_path}/the-history-book-club_member_links', 'r', 'utf-8'):
    user = user.replace('\n', '')
    if user not in user_existing:
        url = 'https://www.goodreads.com' + user
        if url.find('author') == -1:
            print(url)
            driver.get(url)
            html = driver.page_source
            personal_info, personal_ratings = get_user_info(html)
            if personal_info != '':
                user_info_out.write(user + '\t' + personal_info + '\n')
                user_ratings_out.write(user + '\t' + personal_ratings + '\n')
                user_out.write(user + "\n")
            time.sleep(1 + np.random.randint(7))
