import os
import argparse
from unittest import skip

from glados import glados
from messageSender import MessageSender

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--cookie_string", type=str, required=True)

    args= parser.parse_args()
    cookie_string = args.cookie_string
    pushplus_token = os.environ['PUSHPLUS_TOKEN']
    serverChan_sendkey = os.environ['PUSHPLUS_TOKEN']
    weCom_corpId = os.environ['PUSHPLUS_TOKEN']
    weCom_corpSecret = os.environ['PUSHPLUS_TOKEN']
    weCom_agentId = os.environ['PUSHPLUS_TOKEN']
    weCom_tokens = [weCom_corpId, weCom_corpSecret, weCom_agentId]
    if weCom_tokens.count(None) > 0:
        weCom_tokens = [None, None, None]

    message_tokens = {
        "pushplus_token": pushplus_token,
        "serverChan_token": serverChan_sendkey,
        "weCom_tokens": weCom_tokens
    }

    message_sender = MessageSender()

    message_all = str()
    cookie_string = cookie_string.split("&&")
    checkin_codes = list()
    for idx, cookie in enumerate(cookie_string):
        print(f"【Account_{idx+1}】:")
        message_all = f"{message_all}【Account_{idx+1}】:\n\n"
        checkin_code, message = glados(cookie)
        checkin_codes.append(checkin_code)
        message_all = f"{message_all}{message}\n\n"

    message_sender.send_all(message_tokens= message_tokens, title = "GLaDOS Checkin", content = message_all)

    assert -2 not in checkin_codes, "At least one account login fails."
    assert checkin_codes.count(0) + checkin_codes.count(1) == len(checkin_codes), "Not all the accounts check in successfully."
