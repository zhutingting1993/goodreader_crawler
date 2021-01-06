import bs4
from selenium import webdriver
import codecs
import re
import numpy as np
import time
import os


def get_page_num(raw_html):
    read_page = bs4.BeautifulSoup(raw_html, features="html.parser")
    book_shelves = read_page.find_all('div', class_='userShelf')
    read_num, currently_reading_num, want_to_read_num = 0, 0, 0
    for shelf in book_shelves:
        text_str = shelf.find_all('a')[1].get_text()
        if text_str.startswith('Read'):
            read_num = int(text_str.split('(')[1].replace(')', ''))
        elif text_str.startswith('Currently Reading'):
            currently_reading_num = int(text_str.split('(')[1].replace(')', ''))
        elif text_str.startswith('Want to Read'):
            want_to_read_num = int(text_str.split('(')[1].replace(')', ''))

    return read_num, currently_reading_num, want_to_read_num


def get_currently_read_list(driver, page_num, user):
    out_lines = []
    for page in range(1, page_num + 1):
        url = f'https://www.goodreads.com/review/list/{user}?shelf=currently-reading&view=reviews&page={page}'
        print(f'{url}')
        raw_html = driver.get(url).page_source
        out_lines.extend(get_book_info(raw_html))

    return out_lines


def get_read_list(driver, page_num, user):
    out_lines = []
    for page in range(2, page_num + 1):
        url = f'https://www.goodreads.com/review/list/{user}?shelf=read&view=reviews&page={page}'
        print(f'{url}')
        raw_html = driver.get(url).page_source
        out_lines.extend(get_book_info(raw_html))

    return out_lines


def get_book_info(raw_html):
    book_list_html = bs4.BeautifulSoup(raw_html, features="html.parser")
    book_tr = book_list_html.find('table', id='books').find_all('tr', class_='bookalike review')
    out_lines = []
    for book in book_tr:
        title_element = book.find('td', class_='field title').find('a')
        book_title = title_element['title']
        book_href = title_element['href']

        author_element = book.find('td', class_='field author').find('a')

        if author_element is not None:
            author_name = author_element.get_text()
            author_href = author_element['href']
        else:
            author_name = 'unknown'
            author_href = 'unknown'

        avg_rating = float(book.find('td', class_='field avg_rating').find('div', class_='value').get_text())

        date_stated_element = book.find('td', class_='field date_started').find('span', class_='date_started_value')
        date_started = 'None'
        if date_stated_element is not None:
            date_started = book.find('td', class_='field date_started').find('span',
                                                                             class_='date_started_value').get_text()

        date_read_element = book.find('td', class_='field date_read').find('span', class_='date_read_value')
        date_read = 'None'
        if date_read_element is not None:
            date_read = book.find('td', class_='field date_read').find('span', class_='date_read_value').get_text()

        date_added = book.find('td', class_='field date_added').find('span').get_text().replace('\n', '').strip(' ')

        action_link = book.find('td', class_='field actions').find('a', class_='nobreak')['href']

        one_line = f'{book_title}_________{book_href}_________{author_name}_________{author_href}_________{avg_rating}_________{date_started}_________{date_read}_________{date_added}_________{action_link}'

        out_lines.append(one_line)

    return out_lines


def get_list(shelf, num, user, driver):
    out_lines = []

    page_num = num / 20 if num % 20 == 0 else num // 20 + 1

    for page in range(1, int(page_num) + 1):
        url = f'https://www.goodreads.com/review/list/{user}?shelf={shelf}&view=reviews&page={page}'
        print(f'{url}')
        try:
            driver.get(url)
        except:
            print('sleep for a while')
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
            time.sleep(7200)
        raw_html = driver.page_source
        out_lines.extend(get_book_info(raw_html))

        if page % 5 == 0:
            time.sleep(3 + np.random.randint(7))
        elif page % 20 == 0:
            time.sleep(30 + np.random.randint(30))

    return out_lines


if __name__ == '__main__':
    # page_source = codecs.open('d:/test.html', 'r', 'utf-8').read()
    # get_book_info(page_source)
    # # print(page_source)
    #
    # # get total pages
    # read_num, currently_reading_num, want_to_read_num = get_page_num(page_source)
    # print(f'read num:{read_num} {currently_reading_num} {want_to_read_num}')
    #
    # read_page = read_num / 20 if read_num % 20 == 0 else read_num // 20 + 1
    # print(f'read page:{read_page}')
    #
    # user = '/user/show/50620706-alaina'
    #
    # user = user.split('/')[3]
    # # get_read_list(None, read_page, user)
    # get_book_info(page_source)

    # print('time sleep_____________________________')
    # time.sleep(7200 * 2)

    read_out = codecs.open('d:/read', 'a', 'utf-8')
    currently_read_out = codecs.open('d:/currently_read', 'a', 'utf-8')
    want_to_read = codecs.open('d:/want_to_read', 'a', 'utf-8')

    read_out_writers = [read_out, currently_read_out, want_to_read]

    user_ratings_out = codecs.open('d:/user_ratings', 'a', 'utf-8')
    user_existing = []
    if not os.path.exists('d:/user_crawled'):
        # os.mkfifo('d:/user_crawled')
        open('d:/user_crawled', 'a').close()

    for user in codecs.open('d:/user_crawled', 'r', 'utf-8'):
        user_existing.append(user.replace('\n', ''))

    # initial driver
    driver = webdriver.Chrome('C:/Users/DuFei/Downloads/chromedriver_win32/chromedriver')

    driver.get("https://www.goodreads.com/user/sign_in")
    user_name = driver.find_element_by_id('user_email')
    password = driver.find_element_by_id('user_password')

    user_name.send_keys('hfutdufei@gmail.com')
    password.send_keys('df723820')

    login_button = driver.find_element_by_name("next")
    login_button.click()

    user_out = codecs.open('d:/user_crawled', 'a', 'utf-8')

    for user in codecs.open('d:/member_links', 'r', 'utf-8'):
        user = user.replace('\n', '')
        if user not in user_existing:
            user = user.split('/')[3]
            url = f'https://www.goodreads.com/review/list/{user}?shelf=read&view=reviews&page=1'

            print(url)
            try:
                driver.get(url)
            except:
                print('sleep for a while')
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                time.sleep(7200)
            html = driver.page_source

            read_num, currently_reading_num, want_to_read_num = get_page_num(html)

            # shelves = ['read', 'currently-reading', 'to-read']
            shelves = ['read', 'currently-reading']

            nums = [read_num, currently_reading_num, want_to_read_num]

            for index in range(len(shelves)):
                read_list = get_list(shelves[index], nums[index], user, driver)
                for line in read_list:
                    read_out_writers[index].write(f'{user}_________{line}\n')

            user_out.write('/user/show/' + user + "\n")
            time.sleep(1 + np.random.randint(7))
