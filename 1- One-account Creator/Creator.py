from selenium import webdriver
from time import sleep
import passgen
from selenium.webdriver.common.keys import Keys
import requests as r
from bs4 import BeautifulSoup as Bs

def signup(user):
    email = r.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1').json()[0]
    password = passgen.passgen()
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation", 'enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--lang=en")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36")
    options.add_extension('anticaptcha.zip')
    browser = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
    browser.get('chrome://settings/clearBrowserData')
    browser.delete_all_cookies()
    browser.minimize_window()
    browser.get('https://www.reddit.com/register/')
    browser.find_element_by_id('regEmail').send_keys(email)
    browser.find_element_by_id('regEmail').send_keys(Keys.ENTER)
    browser.find_element_by_id('regUsername').send_keys(user)
    browser.find_element_by_id('regPassword').send_keys(password)
    sleep(5)
    while True:
        try:
            status = browser.find_element_by_class_name('status')
            if status.get_attribute("innerHTML") == "Solved":
                break
        except:
            browser.quit()
            return False
    sleep(2)
    browser.find_element_by_id('regPassword').send_keys(Keys.ENTER)
    sleep(3)
    login, domain = email.split('@')
    id_msg = ''
    while True:
        res = r.get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}').json()
        if len(res) > 0:
            id_msg = res[0]['id']
            break
        else:
            sleep(2)
    res = r.get(f'https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={id_msg}').json()
    soup = Bs(res['body'], features='lxml')
    link = soup.find('td', {'class': 'btn-14'}).find('a')['href']
    browser.get(link)
    sleep(5)
    print("Registration Successful")
    browser.quit()
    file = open('accounts.txt', 'a')
    file.write(f'{email}:{user}:{password}\n')
    file.close()
    return True


file = open('usernames.txt', 'r')
username = file.read().splitlines()[0]
file.close()
signup(username)
