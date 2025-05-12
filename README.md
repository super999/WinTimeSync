# WinTimeSync

该项目是一个Windows时间同步工具，使用Python编写。它可以帮助用户将计算机的系统时间与网络时间服务器进行同步。

## 功能
- 获取当前系统时间
- 获取网络时间
- 将系统时间与网络时间进行比较
- 将系统时间与网络时间进行同步

## 使用方法
1. 克隆或下载该项目到本地计算机。
2. 安装所需的依赖库：
   ```bash
   pip install -r requirements.txt
   ```

## 程序打包
- 使用PyInstaller将Python脚本打包为可执行文件，并手动拷贝配置文件到dist目录：
  ```bash
  pyinstaller -i win_time_sync_app.ico --onefile --console --name win_time_sync main.py
  copy config.json dist\
  ```