from selenium.webdriver import Chrome, ChromeOptions

import os
import requests
import datetime

seito_bango = 210510
password = 3094
url = 'https://tsubogawa.cptown.net/'
line_access_token = 'NcHakB54DyxEaS05QE0mJcQq1erDXYVk1E1p627UaCr'
line_api_url = 'https://notify-api.line.me/api/notify'
headers = {'Authorization': 'Bearer ' + line_access_token}

def main():
    """
    キャンセル待ち予約の受付
    """

    driver = set_driver(True)

    Auto_waiting_for_cancellation(driver)


def set_driver(headless_flg):
    options = ChromeOptions()
    if headless_flg == True:
        options.add_argument('--headless')

    return Chrome(options=options) 


def Auto_waiting_for_cancellation(driver):
    driver.get(url)
    while True:
        if datetime.datetime.now().strftime('%H:%M:%S') == '08:00:00':
            if driver.find_element_by_class_name("btn"):
                driver.find_element_by_class_name("btn").click()
            else:
                requests.post(line_api_url, headers=headers, data={'message': 'アクセス出来ませんでした'})
                break
            driver.find_element_by_id("seino").send_keys(seito_bango)
            driver.find_element_by_id("password").send_keys(password)

            choice = driver.find_element_by_id("choice")
            driver.execute_script("arguments[0].click();", choice) 
            driver.find_element_by_class_name("submit-btn").click()
            driver.find_element_by_class_name("bgc-orange").click()
            driver.find_element_by_class_name("submit-btn").click()

            message = {'message': ''}

            if driver.find_elements_by_class_name("card-color01"):
                for i in driver.find_elements_by_class_name("card-color01"):
                    if i.find_element_by_class_name("sel-time").text == '10:30':
                        i.click()
                        break
                driver.find_element_by_class_name("submit-btn").click()

                message['message'] = driver.find_element_by_class_name('data-date').text + '\n'
                message['message'] = message['message'] + driver.find_element_by_class_name('data-time02').text + '\n'
                message['message'] = message['message'] + driver.find_element_by_class_name('data-naiyo02').text

                requests.post(line_api_url, headers=headers, data=message)
            else:
                requests.post(line_api_url, headers=headers, data={'message': '予約は埋まっています'})
            break