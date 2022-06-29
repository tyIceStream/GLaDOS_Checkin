# encoding=utf8
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver as uc
import io
import requests
import base64
import os
import sys
# import time
import json
import subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# server酱开关，填off不开启(默认)，填on同时开启cookie失效通知和签到成功通知
sever = os.environ["SERVE"]

# 填写server酱sckey,不开启server酱则不用填
sckey = os.environ["SERVER_SCKEY"]

# 填入glados账号对应cookie
cookie = os.environ["GLADOS_COOKIE"]

# 企业微信的密钥
wsecret = os.environ["WECHAT_SECRET"]

# 企业ID
wepid = os.environ["ENTERPRISE_ID"]

# 应用ID
appid = os.environ["APP_ID"]


def send_to_wecom(text, wecom_cid, wecom_aid, wecom_secret, wecom_touid='@all'):
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
    response = requests.get(get_token_url).content
    access_token = json.loads(response).get('access_token')
    if access_token and len(access_token) > 0:
        send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        data = {
            "touser": wecom_touid,
            "agentid": wecom_aid,
            "msgtype": "text",
            "text": {
                "content": text
            },
            "duplicate_check_interval": 600
        }
        response = requests.post(send_msg_url, data=json.dumps(data)).content
        return response
    else:
        return False


def send_to_wecom_image(base64_content, wecom_cid, wecom_aid, wecom_secret, wecom_touid='@all'):
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
    response = requests.get(get_token_url).content
    access_token = json.loads(response).get('access_token')
    if access_token and len(access_token) > 0:
        upload_url = f'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=image'
        upload_response = requests.post(upload_url, files={
            "picture": base64.b64decode(base64_content)
        }).json()
        if "media_id" in upload_response:
            media_id = upload_response['media_id']
        else:
            return False

        send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        data = {
            "touser": wecom_touid,
            "agentid": wecom_aid,
            "msgtype": "image",
            "image": {
                "media_id": media_id
            },
            "duplicate_check_interval": 600
        }
        response = requests.post(send_msg_url, data=json.dumps(data)).content
        return response
    else:
        return False


def send_to_wecom_markdown(text, wecom_cid, wecom_aid, wecom_secret, wecom_touid='@all'):
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
    response = requests.get(get_token_url).content
    access_token = json.loads(response).get('access_token')
    if access_token and len(access_token) > 0:
        send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        data = {
            "touser": wecom_touid,
            "agentid": wecom_aid,
            "msgtype": "markdown",
            "markdown": {
                "content": text
            },
            "duplicate_check_interval": 600
        }
        response = requests.post(send_msg_url, data=json.dumps(data)).content
        return response
    else:
        return False


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


def glados_checkin(driver):
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


# 这里的内容并不完善，需要去request这个https://glados.rocks/api/user/status才能拿到traffic(使用量)
    # today = state["data"]["traffic"]
    str = "cookie过期"
    if 'message' in checkin:
        mess = checkin['message']
        # time = state.json()['data']['leftDays']
        # time = time.split('.')[0]
        time = checkin["list"][0]["balance"]
        time = time.split('.')[0]
        # total = 200
        # use = today/1024/1024/1024
        # rat = use/total*100
        # str_rat = '%.2f' % (rat)
        # wecomstr = '提示:%s; 目前剩余%s天; 流量已使用:%.3f/%dGB(%.2f%%)' % (
        #     mess, time, use, total, rat)
        wecomstr = '提示:%s; 目前剩余%s天;' % (
            mess, time)
        # 换成自己的企业微信 idsend_to_wecom_image
        ret = send_to_wecom(wecomstr, wepid, appid, wsecret)
#         ret = send_to_wecom_markdown(wecomstr, wepid , appid , wsecret)
        # str = '%s , you have %s days left. use: %.3f/%dGB(%.2f%%)' % (
        #     mess, time, use, total, rat)
#         ret = send_to_wecom_image(str, wepid , appid , wsecret)
        print(wecomstr)
        if sever == 'on':
            # requests.get('https://sctapi.ftqq.com/' + sckey + '.send?title=' +
            #              mess + '余' + time + '天,用' + str_rat + '%&desp=' + str)
            requests.get('https://sctapi.ftqq.com/' + sckey + '.send?title=' +
                         mess + '余' + time + '天,' + '%&desp=' + str)
    else:
        requests.get('https://sctapi.ftqq.com/' + sckey +
                     '.send?title=Glados_edu_cookie过期')

    # del checkin["list"]
    # print("Time:", time.asctime(time.localtime()), checkin)
    # assert checkin["code"] in [0, 1]


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
    glados_checkin(driver)

    driver.close()
    driver.quit()


if __name__ == "__main__":
    glados(cookie)
