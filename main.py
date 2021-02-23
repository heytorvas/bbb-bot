from bot import *
from access import *

browser = get_browser()
login = set_login(browser, email, password)
page_vote = get_votation_page(login)

while True:
    try:
        vote = set_vote(page_vote)
        checkbox = click_on_checkbox(vote)
        vote_done = get_captcha(checkbox)
        back_again = loop_url_votation(vote_done)
    except:
        print('except')
        browser.quit()
        browser = get_browser()
        login = set_login(browser, email, password)
        page_vote = get_votation_page(login)

        pass