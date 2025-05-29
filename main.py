import paramiko  # SSH 库
import win32api, win32security  # pywin32 库
from datetime import datetime
import json
import argparse
import time
import sys, ctypes


def get_linux_time(host, port, user, passwd):
    """SSH 登录并获取远程 Linux 系统时间（年/月/日/时/分/秒）"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port=port, username=user, password=passwd)  # :contentReference[oaicite:8]{index=8}
    stdin, stdout, _ = client.exec_command("date '+%Y %m %d %H %M %S'")
    parts = stdout.read().decode().strip().split()
    client.close()
    return tuple(map(int, parts))


def set_windows_time(year, month, day, hour, minute, second):
    """启用特权后调用 SetSystemTime 设置 Windows 系统时间（UTC）"""
    # 获取并启用 SE_SYSTEMTIME_NAME 特权
    privilege = win32security.LookupPrivilegeValue(None, win32security.SE_SYSTEMTIME_NAME)
    htok = win32security.OpenProcessToken(win32api.GetCurrentProcess(),
                                          win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY)
    win32security.AdjustTokenPrivileges(htok, False, [(privilege, win32security.SE_PRIVILEGE_ENABLED)])
    # monthDayOfWeek 设置为 0，Windows 会自动计算
    win32api.SetSystemTime(year, month, 0, day, hour, minute, second, 0)  # :contentReference[oaicite:9]{index=9}


def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()


if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

    parser = argparse.ArgumentParser(description='Windows时间同步工具')
    parser.add_argument('--loop', action='store_true', help='是否循环同步')
    args = parser.parse_args()
    print("参数提示: 使用 --loop 参数可循环同步，否则只同步一次。")
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    host = config["host"]
    port = config["port"]
    user = config["user"]
    passwd = config["passwd"]
    sync_interval = config["sync_interval"]
    while True:
        y, m, d, h, mi, s = get_linux_time(host, port, user, passwd)
        set_windows_time(y, m, d, h, mi, s)
        print(f"Windows 时间已同步至 Linux 时间,{y}-{m}-{d} {h}:{mi}:{s}")
        if not args.loop:
            break
        time.sleep(sync_interval)
