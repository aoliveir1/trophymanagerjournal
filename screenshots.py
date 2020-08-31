from decouple import config
from PIL import Image

from utils import create_brower, sign_in

url_base = config('URL_BASE')
"""Initialize browser and log in"""
browser = create_brower()
sign_in(browser, url_base)

links = ['https://trophymanager.com/league/br/1/1/',
         'https://trophymanager.com/league/br/2/1/',
         'https://trophymanager.com/league/br/2/2/',
         'https://trophymanager.com/league/br/2/3/',
         'https://trophymanager.com/league/br/2/4/',
         'https://trophymanager.com/league/pt/1/1/',
         'https://trophymanager.com/league/pt/2/1/',
         'https://trophymanager.com/league/pt/2/2/',
         'https://trophymanager.com/league/pt/2/3/',
         'https://trophymanager.com/league/pt/2/4/']

path = '/full path to store images/'

for link in links:
    img_name = link.replace('/', '')
    img_name = path + img_name[-4:] + '_{}.png'
    browser.visit(link)
    browser.visit(link)
    browser.driver.fullscreen_window()

    #  screenshot on standing table
    table = browser.find_by_css('.column2_a > div:nth-child(1) > div:nth-child(2)')[0]
    table_location = table.__dict__['_element'].location
    table_size = table.__dict__['_element'].size
    browser.driver.save_screenshot(img_name.format('table'))
    x = table_location['x']
    y = table_location['y']
    width = x + table_size['width']
    height = y + table_size['height']
    im = Image.open(img_name.format('table'))
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save(img_name.format('table'))

    #  screenshot on last round results
    last_round = browser.find_by_css('.column3_a > div:nth-child(2) > div:nth-child(2)')[0]
    last_round_location = last_round.__dict__['_element'].location
    last_round_size = last_round.__dict__['_element'].size
    browser.driver.save_screenshot(img_name.format('last_round'))
    x = last_round_location['x']
    y = last_round_location['y']
    width = x + last_round_size['width']
    height = y + last_round_size['height']
    im = Image.open(img_name.format('last_round'))
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save(img_name.format('last_round'))

    # click to see next round and take a screenshot
    browser.find_by_css('#tabnext_round > div:nth-child(1)')[0].click()
    next_round = browser.find_by_css('.column3_a > div:nth-child(2) > div:nth-child(2)')[0]
    next_round_location = next_round.__dict__['_element'].location
    next_round_size = next_round.__dict__['_element'].size
    browser.driver.save_screenshot(img_name.format('next_round'))
    x = next_round_location['x']
    y = next_round_location['y']
    width = x + next_round_size['width']
    height = y + next_round_size['height']
    im = Image.open(img_name.format('next_round'))
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save(img_name.format('next_round'))

browser.quit()
