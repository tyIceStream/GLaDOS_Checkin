import io
import json
import subprocess
import sys
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from wecom import *

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def get_driver_version():
    cmd = r'''powershell -command "&{(Get-Item 'C:\Program Files\Google\Chrome\Application\chrome.exe').VersionInfo.ProductVersion}"'''
    try:
        out, err = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        out = out.decode('utf-8').split(".")[0]
        return out
    except IndexError as e:
        print('Check chrome version failed:{}'.format(e))
        return 0


def get_checkin(driver):
    checkin_url = "https://glados.rocks/api/user/checkin"
    checkin_query = """
        (function (){
        var request = new XMLHttpRequest();
        request.open("POST","%s",false);
        request.setRequestHeader('content-type', 'application/json');
        request.withCredentials=true;
        request.send('{"token": "glados.network"}');
        return request;
        })();
        """ % (checkin_url)
    checkin_query = checkin_query.replace("\n", "")
    resp_checkin = driver.execute_script("return " + checkin_query)
    checkin = json.loads(resp_checkin["response"])
    return checkin["code"], checkin["message"]


def get_Status(driver):
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
    status = json.loads(resp["response"])
    return status["data"]


def glados(cookie_string):
    options = uc.ChromeOptions()
    options.add_argument("--disable-popup-blocking")

    version = get_driver_version()
    driver = uc.Chrome(version_main=version, options=options)

    # Load cookie
    driver.get("https://glados.rocks")

    cookie_dict = [
        {"name": x.split('=')[0].strip(), "value": x[x.find('=')+1:]}
        for x in cookie_string.split(';')
    ]

    driver.delete_all_cookies()
    for cookie in cookie_dict:
        if cookie["name"] in ["koa:sess", "koa:sess.sig", "__stripe_mid", "__cf_bm"]:
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

    checkin_code, checkin_message = get_checkin(driver)
    messages = ""  # code==-2和-100 是默认为空
    if checkin_code != -2:
        if checkin_message != "Please Try Tomorrow":
            status_message = get_Status(driver)
            messages = [checkin_message, status_message]
        else:
            checkin_code = -100  # 意味着已经签到过了

    driver.close()
    driver.quit()

    return checkin_code, messages
