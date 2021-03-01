from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from time import sleep
from util import get_html_page
import requests, pydub, speech_recognition

def get_text_from_audio():
    r = speech_recognition.Recognizer()
    file = speech_recognition.AudioFile('test.wav')

    with file as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)
        result = r.recognize_google(audio, language='en')

    return result

def convert_mp3_to_wav():
    mp3_file = 'audio.mp3'
    wav_file = 'test.wav'

    sound = pydub.AudioSegment.from_mp3(mp3_file)
    sound.export(wav_file, format='wav')

def download_audio_mp3(url):
    doc = requests.get(url)

    with open('audio.mp3', 'wb') as f:
        f.write(doc.content)

def get_browser_recaptha():
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    browser = webdriver.Firefox(options=opts)
    browser.maximize_window()

    browser.delete_all_cookies()
    sleep(2)

    browser.get('https://www.globo.com')
    sleep(2)

    print('browser')
    return browser

def get_iframe_click_login(browser):
    iframes = browser.find_elements_by_tag_name('iframe')
    for i in iframes:
        if i.get_attribute('role').strip() == 'presentation':
            return i

def get_iframe_content_login(browser):
    iframes = browser.find_elements_by_tag_name('iframe')
    for i in iframes:
        if i.get_attribute('title').strip() == 'desafio reCAPTCHA':
            return i

def set_login_recaptha(browser, email, password):
    browser.find_element_by_xpath('/html/body/header/div/div[4]/div[3]/div/div/a').click()
    sleep(2)

    browser.find_element_by_xpath('//*[@id="login"]').send_keys(email)
    browser.find_element_by_xpath('//*[@id="password"]').send_keys(password)
    sleep(1)

    iframe = get_iframe_click_login(browser)
    browser.switch_to.frame(iframe)

    sleep(1)
    browser.find_element_by_id('recaptcha-anchor').click()
    sleep(1)

    browser.switch_to.default_content()
    iframe_content = get_iframe_content_login(browser)
    browser.switch_to.frame(iframe_content)
    sleep(1)

    try:
        browser.find_element_by_xpath('//*[@id="recaptcha-audio-button"]').click()
        sleep(1)
    except:
        pass

    browser.switch_to.default_content()
    iframe_content = get_iframe_content_login(browser)
    browser.switch_to.frame(iframe_content)
    sleep(1)

    while True:
        try:
            soup = get_html_page(browser)
            print(soup)
            audio_url = soup.find('a', {'class': 'rc-audiochallenge-tdownload-link'}).get('href')
            print('audio')

            download_audio_mp3(audio_url)
            convert_mp3_to_wav()
            audio_text = get_text_from_audio()
            print('process')

            browser.find_element_by_xpath('//*[@id="audio-response"]').send_keys(audio_text)
            sleep(1)
            #browser.save_screenshot('printscreen.png')
            browser.find_element_by_xpath('//*[@id="recaptcha-verify-button"]').click()
            sleep(2)

            #browser.save_screenshot('printscreen2.png')
        except:
            break

    browser.switch_to.default_content()
    sleep(1)
    browser.find_element_by_xpath('/html/body/div[1]/main/div[2]/div/div/div/div[2]/div[1]/form/div[6]/button').click()
    sleep(3)
    #browser.save_screenshot('printscreen3.png')

    return browser