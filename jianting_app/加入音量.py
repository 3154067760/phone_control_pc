import pyautogui
import time

# 增大音量（按 5 次音量+）
def volume_up():
    for i in range(5):
        pyautogui.press('volumeup')
        time.sleep(0.1)
    print("✅ 音量已增大")

# 减小音量
def volume_down():
    for i in range(5):
        pyautogui.press('volumedown')
        time.sleep(0.1)
    print("✅ 音量已减小")

# 静音/取消静音
def volume_mute():
    pyautogui.press('volumemute')
    print("✅ 静音切换")

# 测试
volume_up()  # 增大音量
# volume_down()  # 减小音量
# volume_mute()  # 静音