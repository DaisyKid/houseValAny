import csv
import re
import requests
import sys
import io
from bs4 import BeautifulSoup

# 0，小区名
# 1，摇号人数；
# 2，中签数；
# 3，中签比例；
# 4，房子均价
# 5，装修价格
info_list = []
info_total_cnt = 0

def collectHouseInfo(year, month):
    base_url = 'http://www.tmsf.com/yh/2018yh/'
    tail = '_preview.htm'
    date = str(year) + '_' + str(month)
    url = base_url + date + tail
    print("url:", url)
    # url = 'http://www.tmsf.com/yh/2018yh/2018_12_preview.htm'
    headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    html = requests.get(url, headers=headers)
    Soup = BeautifulSoup(html.text,"html.parser")

    if Soup.find('div', class_='content2'):
        all = Soup.find('div', class_='content2').find_all('tr')

    for item in all: #one house
        onehouse = item.find_all('td')
        item_info = []
        for iter in onehouse:
            item_info.append(iter.get_text())
        if len(item_info) > 9:
            house_name = item_info[0]
            house_dic = item_info[1]
            house_provide = item_info[4]
            house_per_price = item_info[5]
            house_per_dec = item_info[6]
            if '毛坯' == item_info[6]:
                house_per_dec = 0
            house_ratio = item_info[9]
            if '/' == item_info[9]:
                house_ratio = 0

            house_info=[date, house_name, house_dic, house_provide, house_per_price, house_per_dec, house_ratio]
            info_list.append(house_info)

def recordToCsv(gbInfo_list):
    with open("test1.csv","w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        #先写入columns_name
        writer.writerow(["date", "house_name", "house_dic", "house_provide", "house_per_price", "house_per_dec", "ratio"])
        #写入多行用writerows，当行用writerow
        for info in gbInfo_list:
            writer.writerow([info[0], info[1], info[2], info[3], info[4], info[5], info[6]])

if __name__ == "__main__":

    for month in range(9, 13):
        collectHouseInfo(2018, month)
    for year in range(2019, 2020):
        for month in range(1, 13):
            collectHouseInfo(year, month)
    for month in range(1, 7):
        collectHouseInfo(2020, month)

    recordToCsv(info_list)