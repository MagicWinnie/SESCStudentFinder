import json
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import etree
from lxml import html
from selenium import webdriver

driver = webdriver.Firefox()

df = pd.DataFrame(columns=['Изображение пользователя', 'Фамилия / Имя'])

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
# ===========SCRAPING==========
driver.get("https://sesc.nsu.ru/edu/moodle/user/index.php?contextid=2&roleid=0&id=1&perpage=100&accesssince=0&search&spage=0")
number_of_pages = int(driver.find_element_by_class_name("last").text)
for i in range(1, number_of_pages):
    # ====GETTING TABLE====
    webpage = driver.page_source

    soup = BeautifulSoup(webpage, features="lxml")
    table = soup.find_all('table')[-1]
    tableTR = table.find_all('tr')
    table = str(table)

    icon = []
    for row in tableTR:
        try:
            icon.append(row.find('img').get('src'))
        except AttributeError:
            continue

    df_local = pd.read_html(table)[0]
    df_local = df_local.rename(columns={'ФамилияСортировать по Фамилия По возрастанию / ИмяСортировать по Имя По возрастанию': 'Фамилия / Имя'})
    df_local = df_local[df_local['Фамилия / Имя'].notna()]
    df_local['Изображение пользователя'] = icon

    df = pd.concat([df, df_local])
    driver.get("https://sesc.nsu.ru/edu/moodle/user/index.php?contextid=2&roleid=0&id=1&perpage=100&accesssince=0&search&spage={}".format(i))

print(df)
df.to_csv('users_raw.csv', index=False, encoding="utf-16")

driver.quit()