import requests
import json
class MessageSender:

    def __init__(self):
        self.sender = {}

        self.register("pushplus_token", self.pushplus)
        self.register("serverChan_token", self.serverChan)
        self.register("weCom_tokens", self.weCom)
        self.register("weCom_webhook", self.weCom_bot)

    def register(self, token_name, callback):
        assert token_name not in self.sender, "Register fails, the token name exists."
        self.sender[token_name] = callback

    def send_all(self, message_tokens, title, content):
        def check_valid_token(token):
            if isinstance(token, type(None)): 
                return False
            if isinstance(token, str) and len(token) == 0:
                return False
            if isinstance(token, list) and (token.count(None) != 0 or token.count("") != 0):
                return False
            return True

        for token_key in message_tokens:
            token_value = message_tokens[token_key]
            if token_key in self.sender and check_valid_token(token_value):
                try:
                    ret = self.sender[token_key](token_value, title, content)
                except:
                    print(f"【Sender】Something wrong happened when handle {self.sender[token_key]}")
                
    def pushplus(self, token, title, content):

        assert type(token) == str, "Wrong type for pushplus token."
        payload = {'token': token, 
                "title": title,
                "content": content, 
                "channel": "wechat",
                "template": "markdown"
                }
        resp = requests.post("http://www.pushplus.plus/send", data=payload)
        resp_json = resp.json()
        if resp_json["code"] == 200:
            print(f"【Pushplus】Send message to Pushplus successfully.")
        if resp_json["code"] != 200:
            print(f"【Pushplus】【Send Message Response】{resp.text}")
            return -1
        return 0

    def serverChan(self, sendkey, title, content):
        assert type(sendkey) == str, "Wrong type for serverChan token." 
        payload = {"title": title,
                "desp": content, 
                }
        resp = requests.post(f"https://sctapi.ftqq.com/{sendkey}.send", data=payload)
        resp_json = resp.json()
        if resp_json["code"] == 0:
            print(f"【ServerChan】Send message to ServerChan successfully.")
        if resp_json["code"] != 0:
            print(f"【ServerChan】【Send Message Response】{resp.text}")
            return -1
        return 0

    def weCom(self, tokens, title, content):
        assert len(tokens) == 3 and tokens.count(None) == 0 and tokens.count("") == 0
        weCom_corpId, weCom_corpSecret, weCom_agentId = tokens

        get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={weCom_corpId}&corpsecret={weCom_corpSecret}"
        resp = requests.get(get_token_url)
        resp_json = resp.json()
        if resp_json["errcode"] != 0:
            print(f"【WeCom】【Get Token Response】{resp.text}")
        access_token = resp_json.get('access_token')
        if access_token is None or len(access_token) == 0:
            return -1
        send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        content = content.replace("\n\n","\n")
        data = {
            "touser": "@all",
            "agentid": weCom_agentId,
            "msgtype": "markdown",
            "markdown": {
                "content": content
            },
            "duplicate_check_interval": 600
        }
        resp = requests.post(send_msg_url, data=json.dumps(data))
        resp_json = resp.json()
        if resp_json["errcode"] == 0:
            print(f"【WeCom】Send message to WeCom successfully.")
        if resp_json["errcode"] != 0:
            print(f"【WeCom】【Send Message Response】{resp.text}")
            return -1
        return 0

    def weCom_bot(self, webhook, title, content):
        assert type(webhook) == str, "Wrong type for WeCom webhook token." 
        assert "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?" in webhook, "Please use the whole webhook url."
        header = {
		    'Content-Type': "application/json"
	    }
        body = {
            "msgtype": "markdown",
		    "markdown": {
			    "content": content
		    }
	    }

        resp = requests.post(webhook, headers = header, data = json.dumps(body))
        resp_json = resp.json()
        if resp_json["errcode"] == 0:
            print(f"【WeCom】Send message to WeCom successfully.")
        if resp_json["errcode"] != 0:
            print(f"【WeCom】【Send Message Response】{resp.text}")
            return -1
        return 0
