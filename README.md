# GLaDOS_Checkin
GLaDOS automatic check-in bypassing CloudFlare using github action

## 功能描述
1. 每日自动进行签到（本项目可通过CloudFlare反爬机制）
2. 支持多用户签到，多个Cookie之间采用`&&`手动分割
3. 支持将签到消息推送至Server酱，Pushplus，企业微信，Bark
4. 本项目可触发Github Notifications，出现Cookie过期/签到失败等可自动发送Email
5. 本项目包含Github Actions keep alive模块，可自动激活Github Actions

## 使用方法

### 1. 添加 Cookie 至 Secrets
- 登陆[GLaDOS](https://glados.rocks/)后，F12打开开发者工具。
- 刷新网页，并在浏览器中提取复制`Cookie`项（本程序可处理`Cookie:`前缀，使用者复制该项时是否具有前缀均可)

<p align="center">
  <img src="imgs/Step1.png" />
</p>

- 在项目页面，依次点击`Settings`-->`Secrets`-->`Actions`-->`New repository secret`
<p align="center">
  <img src="imgs/Step2.png" />
</p>

- 建立名为`GLADOS_COOKIE`的 secret，值为复制的`Cookie`内容，最后点击`Add secret`
- secret名字必须为`GLADOS_COOKIE`，大小写敏感
- 支持多用户签到，多个Cookie之间采用`&&`手动分割完成后填入`GLADOS_COOKIE`即可
- 为保护隐私，不在日志中输出任何Id信息，请自行分辨账号顺序

<p align="center">
  <img src="imgs/Step3.png" />
</p>

### 2. 启用 Actions
- 在项目页面，依次点击`Actions`-->`glados`-->`Run workflow`-->`Run workflow`以激活Actions

<p align="center">
  <img src="imgs/Step4.png" />
</p>

- WorkFlow开启后，每日0时30分自动执行。

## 3. 消息推送 （可选）
本项目支持将签到消息推送至第三方平台，用户选择其希望推送的平台并配置相关token即可。若用户不需要将消息推送至某个（些）平台，则无需对作作出任何配置。

### 3.1 Pushplus
将消息推送至[Pushplus](https://www.pushplus.plus)需手动配置`token`，并在本仓库创建名为`PUSHPLUS_TOKEN`的secret，将`token`作为`PUSHPLUS_TOKEN`的值。

### 3.2 Server酱
将消息推送至[Server酱](https://sct.ftqq.com/sendkey)需手动配置`SendKey`，并在本仓库创建名为`SERVERCHAN_SENDKEY`的secret，将`SendKey`作为`SERVERCHAN_SENDKEY`的值。

### 3.3 企业微信
将消息推送至[企业微信](https://sct.ftqq.com/sendkey)需手动配置群聊机器人`Webhook地址`，并在本仓库创建名为`WECOM_WEBHOOK`的secret，将`Webhook地址`作为`WECOM_WEBHOOK`的值。

- 此处请输入<b>完整</b>的Webhook地址，包含`https://qyapi.weixin.qq.com/cgi-bin/webhook/send?`前缀，无需手动去除，切勿仅输入`key`值。
- 受制于第三方开发者ip访问限制，本项目暂不支持在Github Actions环境中将消息推送至企业微信应用。

### 3.4 Bark
将消息推送至[Bark](https://github.com/Finb/Bark)需手动配置`DeviceKey`，并在本仓库创建名为`BARK_DEVICEKEY`的secret，将`DeviceKey`作为`BARK_DEVICEKEY`的值。


## 鸣谢
- 感谢[yaoysyao](https://github.com/yaoysyao)支持将消息推送至Pushplus的相关内容
- 感谢[AstbReal](https://github.com/AstbReal)支持将消息推送至Server酱和企业微信的相关内容及GLaDOS用户status的解析策略
