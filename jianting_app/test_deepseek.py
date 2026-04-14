import requests
import json

# ====================== 你只需要改这里 ======================
DEEPSEEK_API_KEY = "sk-7a3fa1114739453b8dd29e77c97021e1"


# ==========================================================

def get_ai_command(user_input):
    url = "https://api.deepseek.com/v1/chat/completions"

    # 强化指令：支持多个命令，每行一个，输出列表格式
    prompt = f"""
    你是一个命令识别器。
    只能识别以下操作：
    打开/关闭：pycharm, wechat, doubao
    开机
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
    open startup
    shutdown
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

        # 按行分割，过滤空行，生成命令列表
        command_list = [cmd.strip() for cmd in command_text.splitlines() if cmd.strip()]

        # 空结果返回 [unknown]
        return command_list if command_list else ["unknown"]

    except Exception as e:
        return ["unknown"]


# ====================== 测试 ======================
if __name__ == "__main__":
    print("命令识别系统已启动（输入 exit 退出）")

    while True:
        text = input("\n请输入你的指令：")
        if text == "exit":
            break

        cmd_list = get_ai_command(text)
        print("识别结果（列表）：", cmd_list)