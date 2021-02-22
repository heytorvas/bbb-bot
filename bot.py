from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from util import *
from bs4 import BeautifulSoup
from time import sleep
from detection import get_detection_captcha
import requests

def get_browser():
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    browser = webdriver.Firefox(firefox_options=opts)
    browser.maximize_window()

    browser.get('https://gshow.globo.com/realities/bbb/')

    sleep(2)

    print('browser')
    return browser

def loop_url_votation(browser):
    browser.get('https://gshow.globo.com/realities/bbb/')
    sleep(2)

    return get_votation_page(browser)

def set_login(browser, email, password):
    browser.find_element_by_xpath('//*[@id="barra-item-login"]').click()
    sleep(2)
    browser.find_element_by_xpath('//*[@id="login"]').send_keys(email)
    browser.find_element_by_xpath('//*[@id="password"]').send_keys(password)
    sleep(1)
    browser.find_element_by_xpath('/html/body/div[1]/main/div[2]/div/div/div/div[2]/div[1]/form/div[6]/button').click()
    sleep(3)

    print('login')

    return browser

def get_votation_page(browser):
    soup = get_html_page(browser)
    sleep(3)
    href_url = soup.find('a', {'class': 'bstn-hl-link'}).get('href')

    browser.get(href_url)
    sleep(1)

    print('access page')
    return browser

def set_vote(browser):
    element = browser.execute_script('''
    
        let GHOST_PROPERTIES = [
            { property: 'overflow', value: 'hidden' },
            { property: 'left', value: '-9999px' },
            { property: 'display', value: 'none' },
        ];
        
        let ANCESTOR_MAX_CHILD = 4;
        
        function hasGhostAncestor(childElement, depth) {
            if (hasGhostStyle(childElement.parentNode)) {
            return true;
            }
        
            if (childElement?.parentNode?.childElementCount < ANCESTOR_MAX_CHILD) {
            return hasGhostAncestor(childElement.parentNode);
            }
        
            return false;
        }
        
        function hasGhostStyle(element) {
            const computedStyle =
            element instanceof HTMLElement ? getComputedStyle(element) : null;
        
            if (computedStyle) {
            return GHOST_PROPERTIES.some(
                ({ property, value }) => computedStyle[property] === value
            );
            }
        
            return true;
        }
        
        function findClickableAncestor(element) {
            const computedStyle =
            element instanceof HTMLElement ? getComputedStyle(element) : null;
        
            if (computedStyle?.cursor === 'pointer' && computedStyle?.display === 'flex') {
            return element;
            }
        
            if (element?.parentNode?.childElementCount < ANCESTOR_MAX_CHILD) {
            return findClickableAncestor(element.parentNode);
            }
        
            return null;
        }
        
        function findRealPlayerElement(playerName) {
            const list = Array.from(document.getElementsByTagName('div'))
            .filter(({ innerHTML }) => innerHTML === playerName)
            .filter((element) => !hasGhostAncestor(element));
        
            if (list?.length === 1) {
            return findClickableAncestor(list[0]);
            }
        
            return null;
        }

        return findRealPlayerElement('Karol Conká')

    ''') 

    class_name_tag = element.get_attribute('class')
    browser.find_element_by_class_name(class_name_tag).click()
    sleep(2)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(1)

    print('vote page')
    return browser

def click_on_checkbox(browser):
    iframe = get_iframe_checkbox(browser)
    browser.switch_to.frame(iframe)

    sleep(1)
    browser.find_element_by_id('checkbox').click()
    sleep(1)
    browser.switch_to_default_content()
    sleep(3)

    print('checkbox')
    return browser

def get_iframe_checkbox(browser):
    iframes = browser.find_elements_by_tag_name('iframe')
    for i in iframes:
        if i.get_attribute('title').strip() == 'widget containing checkbox for hCaptcha security challenge':
            return i
    

def get_iframe_content(browser):
    iframes = browser.find_elements_by_tag_name('iframe')
    for i in iframes:
        if i.get_attribute('title').strip() == 'Main content of the hCaptcha challenge':
            return i

def get_captcha(browser):
    print('captcha')
    for loop in range(0, 2):
        iframe_content = get_iframe_content(browser)
        browser.switch_to.frame(iframe_content)

        sleep(2)
        soup = get_html_page(browser)
        captcha_text_pt = soup.find('div', {'class': 'prompt-text'}).text
        captcha_word_en = get_captcha_word(captcha_text_pt)
        print('WORD: {}'.format(captcha_word_en))

        images = soup.find_all('div', {'class': 'image'})
        style_list = []
        for i in images:
            style_list.append(i.get('style'))

        imgs_list = get_url_imgs(style_list)

        for i in range(len(imgs_list)):
            response = requests.get(imgs_list[i])
            file1 = open("images/{}.png".format(i), "wb")
            file1.write(response.content)
            file1.close()

        sleep(1)

        res = get_detection_captcha(captcha_word_en)
        print(res)

        for i in res:
            if res[i] == True:
                browser.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[{}]'.format(i+1)).click()
                print('click')
                sleep(1)

        #browser.save_screenshot('printscreen{}.png'.format(loop))
        browser.find_element_by_xpath('/html/body/div[2]/div[8]').click()
        sleep(2)
        browser.switch_to_default_content()
        sleep(2)

    #browser.save_screenshot('printscreen_final.png')
    print('vote done')

    return browser