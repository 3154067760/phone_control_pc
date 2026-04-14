from flask import Flask
import os
import threading
import time

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

        <button class="btn-green" onclick="location.href='/open_pycharm_run_qq'">🟢 打开PyCharm + 运行关闭QQ</button>
        <button class="btn-blue" onclick="location.href='/open_pycharm'">🔵 仅打开PyCharm</button>

        <button class="btn-red" onclick="location.href='/close_pycharm'">🔴 关闭PyCharm</button>
        <button class="btn-red" onclick="location.href='/close_qq'">🔴 关闭QQ</button>
        <button class="btn-red" onclick="location.href='/close_doubao'">🔴 关闭豆包</button>

        <!-- 关机按钮 -->
        <button class="btn-black" onclick="confirmShutdown()">⚫ 关机</button>
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