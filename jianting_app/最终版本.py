import requests
import json
from flask import Flask, request
import os
import threading
import time
import pyautogui

# ====================== 配置 ======================
DEEPSEEK_API_KEY = "sk-7a3fa1114739453b8dd29e77c97021e1"
app = Flask(__name__)


# ====================== 音量控制函数（你测试成功的版本） ======================
# 增大音量
def volume_up():
    for i in range(5):
        pyautogui.press('volumeup')
        time.sleep(0.1)
    return "🔊 音量已增大"


# 切歌：下一首 (Ctrl + Alt + 右箭头)
def change_music():
    # 同时按下 Ctrl + Alt + 右方向键
    pyautogui.hotkey('ctrl', 'alt', 'right')
    time.sleep(0.2)
    return "🎵 已切换到下一首歌"

# 减小音量
def volume_down():
    for i in range(5):
        pyautogui.press('volumedown')
        time.sleep(0.1)
    return "🔉 音量已减小"

# 静音/取消静音
def volume_mute():
    pyautogui.press('volumemute')
    return "🔇 已切换静音"


# ====================== AI 命令识别（返回列表） ======================
def get_ai_command(user_input):
    url = "https://api.deepseek.com/v1/chat/completions"

    prompt = f"""
    你是一个命令识别器。
    只能识别以下操作：
    切换音乐
    打开/关闭：pycharm, wechat, doubao, qq, soda
    音量：增大, 减小, 静音
    关机

    规则：
    1. 用户输入可能包含 1 个或多个命令
    2. 每个命令单独一行
    3. 只能输出标准命令，不允许任何多余文字、解释、标点
    4. 不认识的命令用 unknown 代替

    允许的标准命令：
    open wechat
    close wechat
    open pycharm
    close pycharm
    open doubao
    close doubao
    open qq
    close qq
    open soda
    close soda
    volume_up
    volume_down
    volume_mute
    shutdown
    change_music
    unknown

    用户输入：{user_input}
    输出标准命令（多个命令分行输出）：
    """

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        command_text = result["choices"][0]["message"]["content"].strip()
        command_list = [cmd.strip() for cmd in command_text.splitlines() if cmd.strip()]
        return command_list if command_list else ["unknown"]
    except Exception as e:
        return ["unknown"]


# ====================== 应用打开/关闭 ======================
@app.route('/open_pycharm')
def open_pycharm():
    try:
        os.startfile(r"D:\software\PyCharm 2025.3\bin\pycharm64.exe")
        return "✅ PyCharm 已打开"
    except:
        return "❌ 打开失败"


@app.route('/close_pycharm')
def close_pycharm():
    os.system("taskkill /f /im pycharm64.exe")
    return "✅ PyCharm 已关闭"


@app.route('/open_qq')
def open_qq():
    try:
        os.startfile(r"D:\software\QQ.exe")
        return "✅ QQ 已打开"
    except:
        return "❌ 打开失败"


@app.route('/close_qq')
def close_qq():
    os.system("taskkill /f /im QQ.exe")
    return "✅ QQ 已关闭"


@app.route('/open_weixin')
def open_weixin():
    try:
        os.startfile(r"C:\Program Files\Tencent\Weixin\Weixin.exe")
        time.sleep(3)
        pyautogui.press('enter')
        return "✅ 微信已打开并自动回车"
    except:
        return "❌ 打开失败"


@app.route('/close_weixin')
def close_weixin():
    os.system("taskkill /f /im Weixin.exe")
    return "✅ 微信已关闭"


@app.route('/open_doubao')
def open_doubao():
    try:
        os.startfile(r"C:\Users\31540\AppData\Local\Doubao\Application\Doubao.exe")
        return "✅ 豆包已打开"
    except:
        return "❌ 打开失败"


@app.route('/close_doubao')
def close_doubao():
    os.system("taskkill /f /im Doubao.exe")
    return "✅ 豆包已关闭"


# -------------------------- 汽水音乐（Soda Music） --------------------------
@app.route('/open_soda')
def open_soda():
    try:
        os.startfile(r"D:\software\Soda Music\SodaMusicLauncher.exe")
        return "✅ 汽水音乐 已打开"
    except:
        return "❌ 打开失败"


@app.route('/close_soda')
def close_soda():
    os.system("taskkill /f /im SodaMusic.exe")
    return "✅ 汽水音乐 已关闭"
# -----------------------------------------------------------------------------------


@app.route('/close_edge')
def close_edge():
    os.system("taskkill /f /im msedge.exe")
    return "✅ Edge 已关闭"


@app.route('/shutdown')
def shutdown():
    os.system("shutdown /s /t 0")
    return "✅ 电脑正在关机..."


# ====================== 核心：接收 AI 列表，自动执行多条命令 ======================
@app.route('/command', methods=['POST'])
def command():
    user_text = request.form['command'].strip()
    cmd_list = get_ai_command(user_text)
    result = []

    for cmd in cmd_list:
        cmd = cmd.lower()

        # 过滤无效命令
        if cmd == "unknown" or cmd == "open startup":
            result.append(f"⏭️ 跳过无效命令：{cmd}")
            continue

        # === 音量控制 ===
        if cmd == "volume_up":
            result.append(volume_up())
            continue
        if cmd == "volume_down":
            result.append(volume_down())
            continue
        if cmd == "volume_mute":
            result.append(volume_mute())
            continue
        if cmd == "change_music":
            result.append(change_music())

        # 关机
        if cmd == "shutdown":
            shutdown()
            result.append("✅ 已执行关机")
            continue

        # 拆分命令
        parts = cmd.split()
        if len(parts) != 2:
            result.append(f"执行成功✅：{cmd}")
            continue

        action, app = parts

        # 打开
        if action == "open":
            if app == 'wechat':
                open_weixin()
                result.append("✅ 已打开 wechat")
                continue
            app_paths = {
                "pycharm": r"D:\software\PyCharm 2025.3\bin\pycharm64.exe",
                "doubao": r"C:\Users\31540\AppData\Local\Doubao\Application\Doubao.exe",
                "qq": r"D:\software\QQ.exe",
                "soda": r"D:\software\Soda Music\SodaMusicLauncher.exe"
            }
            if app in app_paths:
                try:
                    os.startfile(app_paths[app])
                    result.append(f"✅ 已打开 {app}")
                except:
                    result.append(f"❌ 打开失败 {app}")
            else:
                result.append(f"❌ 不支持打开：{app}")

        # 关闭
        elif action == "close":
            app_exes = {
                "pycharm": "pycharm64.exe",
                "wechat": "Weixin.exe",
                "doubao": "Doubao.exe",
                "qq": "QQ.exe",
                "edge": "msedge.exe",
                "soda": "SodaMusic.exe"
            }
            if app in app_exes:
                os.system(f"taskkill /f /im {app_exes[app]}")
                result.append(f"✅ 已关闭 {app}")
            else:
                result.append(f"❌ 不支持关闭：{app}")

    return "<br>".join(result)


# ====================== 手机前端页面 ======================
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI 控制电脑</title>
        <style>
            body{text-align:center; margin-top:50px; background:#f5f5f5; font-family:Arial;}
            textarea,button{width:85%; padding:15px; margin:10px; font-size:18px; border-radius:8px;}
            button{background:#007bff; color:white; border:none;}
        </style>
    </head>
    <body>
        <h2>🤖手机 AI 控制电脑（支持音量）</h2>
        <form action="/command" method="post">
            <textarea name="command" rows="5" placeholder="支持：
打开汽水音乐，切歌
加大音量，
静音
关闭微信
关机"></textarea>
            <button type="submit">🚀 执行</button>
        </form>
    </body>
    </html>
    '''


# ====================== 启动服务 ======================
def run_server():
    app.run(host='0.0.0.0', port=5000, debug=False)


if __name__ == '__main__':
    threading.Thread(target=run_server, daemon=True).start()
    print("✅ 服务已启动，手机访问电脑IP:5000 即可控制")
    while True:
        time.sleep(1)