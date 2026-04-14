from flask import Flask
import os
import time

app = Flask(__name__)

# 彻底关闭微信（终极版）
@app.route('/close_wechat')
def close_wechat():
    os.system("taskkill /f /im WeChatAppEx.exe")
    time.sleep(0.3)
    os.system("taskkill /f /im Weixin.exe")
    time.sleep(0.3)
    os.system("taskkill /f /im WeChat.exe")
    return "✅ 微信已彻底关闭"

# 关闭 QQ
@app.route('/close_qq')
def close_qq():
    os.system("taskkill /f /im QQ.exe")
    os.system("taskkill /f /im TIM.exe")
    return "✅ 已关闭 QQ"

# 关闭浏览器
@app.route('/close_browser')
def close_browser():
    os.system("taskkill /f /im chrome.exe")
    os.system("taskkill /f /im msedge.exe")
    return "✅ 已关闭浏览器"

# 🔴 关闭 PyCharm（你要的功能！）
@app.route('/close_pycharm')
def close_pycharm():
    os.system("taskkill /f /im pycharm64.exe")
    return "✅ PyCharm 已关闭"

@app.route('/close_doubao')
def close_pycharm():
    os.system("taskkill /f /im Doubao.exe")
    return "✅ PyCharm 已关闭"

# 手机控制面板
@app.route('/')
def control_panel():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>手机控制电脑</title>
        <style>
            body{text-align:center;margin-top:30px;background:#f5f5f5;}
            button{
                width:85%;padding:22px;margin:10px;
                font-size:22px;border:none;border-radius:12px;
                background:#ff4444;color:white;
            }
        </style>
    </head>
    <body>
        <h2>📱 手机远程关闭软件</h2>
        <button onclick="window.location.href='/close_wechat'">关闭微信</button>
        <button onclick="window.location.href='/close_wechat'">关闭豆包</button>
        <button onclick="window.location.href='/close_qq'">关闭QQ</button>
        <button onclick="window.location.href='/close_browser'">关闭浏览器</button>
        <button onclick="window.location.href='/close_pycharm'">🔴 关闭 PyCharm</button>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)