from selenium import webdriver
from time import sleep
import passgen
from selenium.webdriver.common.keys import Keys
import requests as r
from bs4 import BeautifulSoup as Bs
import sys
from requests import Session

redirect_domain = 'https://google.com'

# splitting proxies and saving to proxy_phrases file
with open('proxies.txt', 'r') as reader:
    proxies_to_separate = reader.read().strip().split('\n')
    for proxy in proxies_to_separate:
        proxy = proxy.split(':')
        PROXY_IP = proxy[0]
        PROXY_PORT = proxy[1]
        PROXY_IP_and_PORT = PROXY_IP + ":" + PROXY_PORT
        PROXY_USER = proxy[2]
        PROXY_PASS = proxy[3]
        proxy_phrase = "http://" + PROXY_USER + ":" + PROXY_PASS + "@" + PROXY_IP_and_PORT
        file = open('proxy_phrases.txt', 'a')
        file.write(f'{proxy_phrase}\n')
        file.close()

# main function of registering the account and verifying through email api
def signup(user):
    session = Session()
    session.proxies['http'] = str(proxy_phrase)
    ext_ip = session.get('http://checkip.dyndns.org')
    current_ip = ext_ip.text
    print(current_ip)
    email = r.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1').json()[0]
    password = passgen.passgen()
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation", 'enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--lang=en")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36")
    options.add_extension('anticaptcha.zip')
    browser = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
    browser.minimize_window()
    browser.get('chrome://settings/clearBrowserData')
    browser.find_element_by_xpath('//settings-ui').send_keys(Keys.ENTER)
    browser.delete_all_cookies()
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

    sleep(5)
    session.close()
    browser.quit()
    file = open('accounts.txt', 'a')
    file.write(f'{email}:{user}:{password}\n')
    file.close()
    return True


# unpacking data files to zip together
file = open('usernames.txt', 'r')
usernames = file.read().splitlines()
file.close()

file = open('proxy_phrases.txt', 'r')
phrases = file.read().splitlines()
file.close()

# defining the dictionary
creds = {'usernames': [], 'proxy_phrases': []}

# iterating over user names and proxy phrases to register the accounts
for user, phrase in creds.items():
    with open(f"{user}.txt") as fp:
        creds.update({user: fp.read().splitlines()})
        creation_creds = list(zip(creds['usernames'], creds['proxy_phrases']))
    for one in creation_creds:
        getting_proxy = one[1]
        register_user = one[0]

        # session = Session()
        # session.proxies['https'] = str(getting_proxy)
        # response = session.get("https://reddit.com")
        # print("URL Response: ", response)

        signup(register_user)
        print("Successfully Registered ", register_user)
        sleep(900)