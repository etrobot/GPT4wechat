# GPT4wechat
将new bing的gpt-4和微信结合形成私人助理

步骤：
首先你需要登录有new bing资格的账号，使用cookie editor导出cookies.json保存到项目目录；
然后运行pip install -r requirements.txt安装所需要的库，最后运行gpt4wechat.py即可。
注意：如果微信提示新设备登录倒数5秒，需要在GPT4wechat/venv/lib/python3.9/site packages/itchat/components/login.py找到『'please press confirm on your phone.'』,加入一行『time.sleep(10)』再重新运行即可。
