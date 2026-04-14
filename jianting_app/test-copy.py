from flask import Flask, request
import os
import threading
import time
import pyautogui  # 自动按键库

app = Flask(__name__)


# 1. 仅打开PyCharm
@app.route('/open_pycharm')
def open_pycharm():
    try:
        pycharm_path = r"D:\software\PyCharm 2025.3\bin\pycharm64.exe"
        os.startfile(pycharm_path)
        return "✅ PyCharm 已打开"
    except Exception as e:
        return f"❌ 打开失败：{str(e)}"


# 2. 打开PyCharm + 自动运行关闭QQ脚本
@app.route('/open_pycharm_run_qq')
def open_pycharm_run_qq():
    try:
        pycharm_path = r"D:\software\PyCharm 2025.3\bin\pycharm64.exe"
        os.startfile(pycharm_path)
        time.sleep(2)
        qq_script_path = r"C:\Users\31540\PycharmProjects\shouji_close_computerApp\jianting_app\关闭QQ.py"
        os.system(f'python "{qq_script_path}"')
        return "✅ 已打开PyCharm，并自动运行「关闭QQ.py」"
    except Exception as e:
        return f"❌ 操作失败：{str(e)}"


# 3. 关闭PyCharm
@app.route('/close_pycharm')
def close_pycharm():
    os.system("taskkill /f /im pycharm64.exe")
    return "✅ PyCharm 已关闭"


# 4. 关闭QQ
@app.route('/close_qq')
def close_qq():
    os.system("taskkill /f /im QQ.exe")
    return "✅ QQ 已关闭"


# 5. 关闭豆包
@app.route('/close_doubao')
def close_doubao():
    os.system("taskkill /f /im Doubao.exe")
    return "✅ 豆包 已关闭"


# 6. 电脑关机（新增）
@app.route('/shutdown')
def shutdown():
    os.system("shutdown /s /t 0")
    return "✅ 电脑正在关机..."


# -------------------------- 打开微信 + 自动回车 --------------------------
@app.route('/open_weixin')
def open_weixin():
    try:
        weixin_path = r"C:\Program Files\Tencent\Weixin\Weixin.exe"
        os.startfile(weixin_path)

        # 等待微信窗口加载出来（可根据你电脑速度调整时间）
        time.sleep(3)

        # 自动按 回车键
        pyautogui.press('enter')

        return "✅ 微信已打开，并自动按下回车键"
    except Exception as e:
        return f"❌ 打开失败：{str(e)}"


# -------------------------- 打开豆包 --------------------------
@app.route('/open_doubao')
def open_doubao():
    try:
        # 严格对应你截图中的路径
        doubao_path = r"C:\Users\31540\AppData\Local\Doubao\Application\Doubao.exe"
        os.startfile(doubao_path)
        return "✅ 豆包 已打开"
    except Exception as e:
        return f"❌ 打开失败：{str(e)}"


# -------------------------- ✅ 新增：关闭微信功能 --------------------------
@app.route('/close_weixin')
def close_weixin():
    os.system("taskkill /f /im Weixin.exe")
    return "✅ 微信 已关闭"
# -------------------------------------------------------------------------


# -------------------------- ✅ 新增：关闭Microsoft Edge浏览器 --------------------------
@app.route('/close_edge')
def close_edge():
    os.system("taskkill /f /im msedge.exe")
    return "✅ Microsoft Edge 浏览器 已关闭"
# -----------------------------------------------------------------------------------


@app.route('/command', methods=['POST'])
def command():
    cmd = request.form['command'].strip().lower()
    if cmd == 'shutdown':
        return shutdown()

    parts = cmd.split()
    if len(parts) == 2:
        action, app = parts
        if action == 'open':
            known_apps = {
                'pycharm': r"D:\software\PyCharm 2025.3\bin\pycharm64.exe",
                'wechat': r"C:\Program Files\Tencent\Weixin\Weixin.exe",
                'doubao': r"C:\Users\31540\AppData\Local\Doubao\Application\Doubao.exe"
            }
            if app in known_apps:
                try:
                    os.startfile(known_apps[app])
                    return f"✅ {app} 已打开"
                except Exception as e:
                    return f"❌ 打开失败：{str(e)}"
            else:
                try:
                    os.startfile(app)
                    return f"✅ {app} 已打开"
                except Exception as e:
                    return f"❌ 无法打开 {app}：{str(e)}"
        elif action == 'close':
            known_exes = {
                'pycharm': 'pycharm64.exe',
                'qq': 'QQ.exe',
                'doubao': 'Doubao.exe',
                'wechat': 'Weixin.exe',
                'edge': 'msedge.exe'
            }
            if app in known_exes:
                exe = known_exes[app]
            else:
                exe = f"{app}.exe"
            os.system(f"taskkill /f /im {exe}")
            return f"✅ {app} 已关闭"
        else:
            return "❌ 无效动作。使用 'open app' 或 'close app'"
    else:
        return "❌ 命令格式：'open app', 'close app', 或 'shutdown'"


# 手机控制面板
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>手机控制电脑</title>
        <style>
            body{text-align:center; margin-top:50px; background:#f5f5f5; font-family:Arial;}
            h2{color:#333; margin-bottom:30px;}
            input[type="text"]{
                width:80%; padding:15px; margin:10px;
                font-size:20px; border:2px solid #ccc; border-radius:8px;
            }
            button{
                width:85%; padding:20px; margin:10px;
                font-size:22px; border:none; border-radius:12px;
                color:white; cursor:pointer; font-weight:bold;
            }
            .btn-green{background:#28a745;}
            .btn-blue{background:#007bff;}
            .btn-red{background:#dc3545;}
            .btn-black{background:#000000;}
            button:active{opacity:0.9;}
        </style>
        <script>
            function confirmShutdown(){
                if(confirm("确定要关机吗？")){
                    location.href='/shutdown';
                }
            }
        </script>
    </head>
    <body>
        <h2>📱 手机控制电脑</h2>
        
        <form action="/command" method="post">
            <input type="text" name="command" placeholder="输入命令，如 'open wechat' 或 'close pycharm'" required>
            <button type="submit" class="btn-blue">执行命令</button>
        </form>
        
        <p>命令格式：'open app', 'close app', 或 'shutdown'</p>
    </body>
    </html>
    '''


# 后台运行服务
def run_server():
    app.run(host='0.0.0.0', port=5000, debug=False)


if __name__ == '__main__':
    threading.Thread(target=run_server, daemon=True).start()
    while True:
        time.sleep(1)