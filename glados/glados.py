# encoding=utf8
import io
import re
import sys
import time
import json
import subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

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
        request.withCredentials=true;
        request.send('{"token": "glados.network"}');
        return request;
        })();
        """ % (checkin_url)
    checkin_query = checkin_query.replace("\n", "")
    resp = driver.execute_script("return " + checkin_query)
    resp = json.loads(resp["response"])
    return resp["code"], resp["message"]

def glados(cookie_string):
    options = uc.ChromeOptions()
    options.add_argument("--disable-popup-blocking")
      
    version = get_driver_version()
    driver = uc.Chrome(version_main = version, options = options)

    # Load cookie
    driver.get("https://glados.rocks")

    cookie_dict = [ 
        {"name": x[:x.find('=')].strip(), "value": x[x.find('=')+1:].strip()} 
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
    code, message = glados_checkin(driver)
    print(f"【Log】{message}")
    assert code != -2, f"{message}，请检查Cookie"
    assert code in [0,1]

    driver.close()
    driver.quit()
    
if __name__ == "__main__":
    cookie_string = sys.argv[1]
    
    glados(cookie_string)
