# GLaDOS_Checkin
GLaDOS automatic check-in bypassing CloudFlare using github action

## 功能描述
1. 每日自动进行签到（本项目可通过CloudFlare反爬机制）
2. 支持多用户签到，多个Cookie之间采用`&&`手动分割
3. 本项目包含Github Actions keep alive模块，可自动激活Github Actions

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

- 本项目由Workflow控制，每日0时30分自动执行。
- 本项目目前可以正常运行，如果有其他使用问题请在Issues留言。
