from crawler.login_util import login_good_read

import codecs
import time
import os
import numpy as np

import bs4


# craw page num of member list
def get_group_member_page_count(member_page_raw_html):
    member_page = bs4.BeautifulSoup(member_page_raw_html, features="html.parser")
    max_page_num = member_page.find(name='span', class_="previous_page").find_parent('div')['max_num_pages']
    return int(max_page_num)


# craw member link list
def get_member_links(member_page_raw_html):
    member_page = bs4.BeautifulSoup(member_page_raw_html, features="html.parser")
    member_links = []
    for member_element in member_page.find_all('div', class_='elementList'):
        member_links.append(member_element.find('a', class_='userName')['href'])

    return member_links


def save_list(output_file, list_object):
    out = codecs.open(output_file, 'a', 'utf-8')

    for link in list_object:
        out.write(link + '\n')


def read_list_number(input_file):
    if not os.path.exists(input_file):
        return 0

    out = codecs.open(input_file, 'r', 'utf-8')
    count = 0
    for link in out:
        count += 1
    return count


if __name__ == "__main__":

    # test_search_in_python_org()
    # local_page_path = 'd:/group_member.html'

    group_info = {
        # 'retro-chapter-chicks': 'https://www.goodreads.com/group/136464-retro-chapter-chicks/members',
        # 'the-napoleonic-wars': 'https://www.goodreads.com/group/20116-the-napoleonic-wars/members',
        # 'Club_de_novela_histórica': 'https://www.goodreads.com/group/960211-club-de-novela-hist-rica/members',
        # 'wholesome-history-reads-group': 'https://www.goodreads.com/group/148604-wholesome-history-reads-group/members',
        # 'the-history-book-club': 'https://www.goodreads.com/group/8115-the-history-book-club/members',
        # 'old-books-new-readers': 'https://www.goodreads.com/group/66953-old-books-new-readers/members',
        'spirits-a-drunken-dive-into-myths-and-legends': 'https://www.goodreads.com/group/205387-spirits-a-drunken-dive-into-myths-and-legends/members'
    }

    # group_member_link = 'https://www.goodreads.com/group/142309-underground-knowledge-a-discussion-group/members'

    pre_path = 'D:/OneDrive/工作目录/00A TT/paper2/data/goodread/'

    for g_info in group_info:

        print(g_info)
        print(group_info[g_info])
        group_member_link = group_info[g_info]

        member_links = []

        # initial driver
        driver = login_good_read()

        # member list page 1
        # driver.get(group_member_link)
        # member_page_raw_html = driver.page_source

        # member_links.extend(get_member_links(member_page_raw_html))

        # member_page_raw_html = open(local_page_path, encoding='utf-8').read()
        # print(member_page_raw_html)

        # member_list_page_num = get_group_member_page_count(member_page_raw_html)

        save_file = f'{pre_path}/{g_info}_member_links'
        start_page = int(read_list_number(save_file) / 30)
        print('start page:' + str(start_page))

        for page in range(start_page, 21):
            current_link = group_member_link + "?page=" + str(page)
            driver.get(current_link)
            # print(driver.page_source)
            current_links = get_member_links(driver.page_source)
            print(str(page) + '\tcurrent:' + str(len(current_links)))
            member_links.extend(current_links)
            save_list(save_file, member_links)
            member_links = []
            time.sleep(1 + np.random.randint(5))
            # break

        print(len(member_links))
