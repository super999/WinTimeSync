import paramiko  # SSH 库
import win32api, win32security  # pywin32 库
from datetime import datetime


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


if __name__ == "__main__":
    # 请根据实际环境替换以下参数
    host, port = "192.168.9.136", 22
    user, passwd = "super999", "chenxiawen"
    y, m, d, h, mi, s = get_linux_time(host, port, user, passwd)
    set_windows_time(y, m, d, h, mi, s)
    print(f"Windows 时间已同步至 Linux 时间,{y}-{m}-{d} {h}:{mi}:{s}")
