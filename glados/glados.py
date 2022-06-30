# encoding=utf8
import io
import re
import sys
import time
import json
import subprocess
import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait


def get_driver_version():
    cmd = r'''powershell -command "&{(Get-Item 'C:\Program Files\Google\Chrome\Application\chrome.exe').VersionInfo.ProductVersion}"'''
    try:
        out, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        out = out.decode('utf-8').split(".")[0]
        return out
    except IndexError as e:
        print('Check chrome version failed:{}'.format(e))
        return 0


def glados_checkin(driver):
    checkin_url = "https://glados.rocks/api/user/checkin"
    checkin_query = """
        (function (){
        var request = new XMLHttpRequest();
        request.open("POST","%s",false);
        request.setRequestHeader('content-type', 'application/json');
        request.send('{"token": "glados.network"}');
        return request;
        })();
        """ % (checkin_url)
    checkin_query = checkin_query.replace("\n", "")
    resp = driver.execute_script("return " + checkin_query)
    resp = json.loads(resp["response"])
    return resp["code"], resp["message"]


def glados_status(driver):
    status_url = "https://glados.rocks/api/user/status"
    status_query = """
        (function (){
        var request = new XMLHttpRequest();
        request.open("GET","%s",false);
        request.send(null);
        return request;
        })();
        """ % (status_url)
    status_query = status_query.replace("\n", "")
    resp = driver.execute_script("return " + status_query)
    resp = json.loads(resp["response"])
    return resp["code"], resp["data"]


def pushplus_message(token, message):
    payload = {'token': token, "channel": "wechat", "template": "html", "title": "签到状态", "content": message}
    resp = requests.post("http://www.pushplus.plus/send", params=payload)
    print(resp.status_code)
    resp.close()


def glados(cookie_string, pushplus_token=None):
    options = uc.ChromeOptions()
    options.add_argument("--disable-popup-blocking")

    version = get_driver_version()
    driver = uc.Chrome(version_main=version, options=options)

    # Load cookie
    driver.get("https://glados.rocks")

    if cookie_string.startswith("cookie:"):
        cookie_string = cookie_string[len("cookie:"):]
    cookie_dict = [
        {"name": x[:x.find('=')].strip(), "value": x[x.find('=') + 1:].strip()}
        for x in cookie_string.split(';')
    ]

    driver.delete_all_cookies()
    for cookie in cookie_dict:
        if cookie["name"] in ["koa:sess", "koa:sess.sig"]:
            driver.add_cookie({
                "domain": "glados.rocks",
                "name": cookie["name"],
                "value": cookie["value"],
                "path": "/",
            })

    driver.get("https://glados.rocks")
    WebDriverWait(driver, 240).until(
        lambda x: x.title != "Just a moment..."
    )

    checkin_code, checkin_message = glados_checkin(driver)
    if checkin_code == -2: checkin_message = "Login fails, please check your cookie."
    print(f"【Checkin】{checkin_message}")

    if checkin_code != -2:
        status_code, status_data = glados_status(driver)
        left_days = int(float(status_data["leftDays"]))
        print(f"【Status】Left days:{left_days}")
        if pushplus_token is not None and len(pushplus_token) > 0:
            pushplus_message(pushplus_token, '【Checkin】' + checkin_message + ',【Status】Left days:' + str(left_days) + ',[email]' + status_data["email"])

    driver.close()
    driver.quit()

    return checkin_code


if __name__ == "__main__":
    cookie_string = sys.argv[1]
    pushplus_token = sys.argv[2]
    assert cookie_string
    assert pushplus_token

    cookie_string = cookie_string.split("&&")
    checkin_codes = list()
    for idx, cookie in enumerate(cookie_string):
        print(f"【Account_{idx + 1}】:")
        checkin_code = glados(cookie, pushplus_token=pushplus_token)
        checkin_codes.append(checkin_code)

    assert -2 not in checkin_codes, "At least one account login fails."
    assert checkin_codes.count(0) + checkin_codes.count(1) == len(checkin_codes), "Not all the accounts check in successfully."
