from bs4 import BeautifulSoup

def get_html_page(browser):
    data = browser.find_element_by_tag_name('body')
    html = data.get_attribute('innerHTML')
    return BeautifulSoup(html, 'html.parser')

def get_url_imgs(imgs):
    imgs_urls = []

    for i in imgs:
        if 'url' in i:
            aux = i.split('url("')
            x = aux[1].split('")')
            imgs_urls.append(x[0])

    img_urls_done = []
    for i in range(3, len(imgs_urls)):
        img_urls_done.append(imgs_urls[i])

    return img_urls_done

def get_captcha_word(phrase):
    words_list = phrase.split()
    captcha_text_pt = words_list[-1].strip()

    if captcha_text_pt == 'bicicleta':
        return 'bicycle'
    if captcha_text_pt == 'barco':
        return 'boat'
    else:
        return None