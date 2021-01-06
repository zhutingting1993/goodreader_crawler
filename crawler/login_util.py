from selenium import webdriver


def login_good_read():
    driver = webdriver.Chrome('d:/program files/chromedriver')

    driver.get("https://www.goodreads.com/user/sign_in")
    user_name = driver.find_element_by_id('user_email')
    password = driver.find_element_by_id('user_password')

    user_name.send_keys('Please specific your GoodReads username here')
    password.send_keys('The password')

    login_button = driver.find_element_by_name("next")
    login_button.click()

    return driver


# 直接获取一个driver
def get_general_driver():
    driver = webdriver.Chrome('d:/program files/chromedriver')

    return driver
