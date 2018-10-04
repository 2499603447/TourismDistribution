import os
from tqdm import tqdm
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
import pandas as pd

position = ["南京", "安徽"]

name, level, stars_level, address, sold_tickets = [], [], [], [], []

def get_one_page(key, page):
    try:
        # Open the chrome web window
        chromedriver = "C:\\Dezhou\\install\\chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        driver = webdriver.Chrome(chromedriver)

        url = "http://piao.qunar.com/ticket/list.htm?keyword=" + str(
            key) + "&region=&from=mpl_search_suggest&page=" + str(page)
        driver.get(url)
        data = driver.find_elements_by_class_name("sight_item")
        for i in range(len(data)):
            # get sight's name
            name.append(data[i].find_element_by_class_name("name").text)
            # get sight's level
            try:
                level.append(data[i].find_element_by_class_name("level").text)
            except:
                level.append("")
            # get sight's star level
            stars_level.append(data[i].find_element_by_class_name("product_star_level").text[3:])
            # get sight's position
            address.append(data[i].find_element_by_class_name("area").text)
            # get sight's tickets/month
            try:
                sold_tickets.append(data[i].find_element_by_class_name("hot_num").text)
            except:
                sold_tickets.append(0)

        driver.quit()
        return
    except TimeoutException or WebDriverException:
        return get_one_page()


for key in tqdm(position):
    print("Getting {} data...".format(key))
    for page in range(1, 11):
        print("getting page {}".format(page))
        get_one_page(key, page)

tourism_sight = {'name': name, 'level': level, 'stars_level': stars_level, 'address': address, 'sold_tickets': sold_tickets}
tourism_sight = pd.DataFrame(sight, columns=['name', 'level', 'stars_level', 'address', 'sold_tickets'])
tourism_sight.to_csv("sight.csv", encoding="utf_8_sig")
