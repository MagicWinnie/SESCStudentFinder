import os
import sys
import json
import requests
from pathlib import Path
import pandas as pd
from selenium import webdriver

args = sys.argv

if len(args) != 2:
    print("Usage: python scraping_images.py where/to/save")
    exit(-1)

SAVE_PATH = args[-1]

if not(os.path.isdir(SAVE_PATH)):
    print("Save path does not exist")
    exit(-1)

d = json.load(open('data.json', 'r', encoding='utf-8'))

driver = webdriver.Firefox()
# ============LOGIN============
login_data = json.load(open("website_login_data.json", "r"))

driver.get("https://sesc.nsu.ru/edu/moodle/login/index.php")

username = driver.find_element_by_id("username")
username.clear()
username.send_keys(login_data["login"])

password = driver.find_element_by_id("password")
password.clear()
password.send_keys(login_data["password"])

driver.find_element_by_id("loginbtn").click()

# F:/magic/Documents/SESC_STUDENTS/MOODLE

# ========DOWNLOADING IMAGES=======
for key in d:
    Path(os.path.join(SAVE_PATH, key)).mkdir(parents=True, exist_ok=True)

    df = pd.read_csv('csv_classes/{}.csv'.format(key), encoding='utf-16')

    paths = []

    for i in df.itertuples():
        driver.get(i._4)

        with open(os.path.join(SAVE_PATH, key, i.Index + ".png"), 'wb') as handle:
            handle.write(driver.find_element_by_tag_name('img').screenshot_as_png)
        # print(os.path.join(SAVE_PATH, key, str(i.Index) + ".png"))
        paths.append(os.path.join(SAVE_PATH, key, str(i.Index) + ".png"))

    df['Пути к изображениям'] = paths
    df.to_csv('csv_classes/{}.csv'.format(key), index=False, encoding='utf-16')

driver.quit()