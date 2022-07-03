import argparse

from glados import glados
from messageSender import MessageSender

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--cookie_string", type=str, required=True)
    parser.add_argument("--pushplus_token", type=str)
    parser.add_argument("--serverChan_sendkey", type=str)
    parser.add_argument("--weCom_corpId", type=str)
    parser.add_argument("--weCom_corpSecret", type=str)
    parser.add_argument("--weCom_agentId", type=str)

    get_valid_arg = lambda x: x if x is not None and len(x)>0 else None
    args = parser.parse_args()
    cookie_string = args.cookie_string
    pushplus_token = get_valid_arg(args.pushplus_token)
    serverChan_sendkey = get_valid_arg(args.serverChan_sendkey)
    
    weCom_corpId = get_valid_arg(args.weCom_corpId)
    weCom_corpSecret = get_valid_arg(args.weCom_corpSecret)
    weCom_agentId = get_valid_arg(args.weCom_agentId)
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
        checkin_code, message = glados(cookie, message_tokens)
        checkin_codes.append(checkin_code)
        message_all = f"{message_all}{message}\n\n"

    message_sender.send_all(message_tokens= message_tokens, title = "GLaDOS Checkin", content = message_all)

    assert -2 not in checkin_codes, "At least one account login fails."
    assert checkin_codes.count(0) + checkin_codes.count(1) == len(checkin_codes), "Not all the accounts check in successfully."
