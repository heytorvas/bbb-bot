from bot import *
from access import *
from recaptcha_solver import *

browser = get_browser_recaptha()
login = set_login_recaptha(browser, email, password)
bbb_page = access_bbb_page(login)
page_vote = get_votation_page(bbb_page)
total_vote = 0

while True:
    try:
        vote = set_vote(page_vote)
        checkbox = click_on_checkbox(vote)
        vote_done = get_captcha(checkbox)
        back_again = loop_url_votation(vote_done)
        total_vote += 1
        print('total votes: {}'.format(total_vote))
        
    except:
        print('except')
        bbb_page = access_bbb_page(login)
        page_vote = get_votation_page(bbb_page)
        pass