#!/usr/bin/env python3
import subprocess
import sys
import os
import platform

def get_env_type():
    """精准识别环境类型：zerotermux/windows/macos/linux"""
    # 优先判断 ZeroTermux（Termux 特有标识）
    if "TERMUX_VERSION" in os.environ or "/data/data/com.termux/" in os.path.expanduser("~"):
        return "zerotermux"
    sys_name = platform.system()
    if sys_name == "Windows":
        return "windows"
    elif sys_name == "Darwin":
        return "macos"
    elif sys_name == "Linux":
        return "linux"
    else:
        return "unknown"

def install_python():
    print("=== 双环境 Python 一键安装工具（精准版）===")
    env_type = get_env_type()
    print(f"当前环境：{env_type}")

    try:
        # 1. ZeroTermux 环境（用 pkg 命令）
        if env_type == "zerotermux":
            print("\n[1/3] 更新软件源...")
            subprocess.run(["pkg", "update", "-y"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
            print("[2/3] 安装 Python...")
            subprocess.run(["pkg", "install", "python", "-y"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
            print("[3/3] 验证安装...")
            py_ver = subprocess.run(["python", "--version"], stdout=subprocess.PIPE, text=True).stdout.strip()
            pip_ver = subprocess.run(["pip", "--version"], stdout=subprocess.PIPE, text=True).stdout.strip()
            print(f"\n🎉 安装成功！Python：{py_ver}\npip：{pip_ver}")

        # 2. Windows 环境（给出官方安装指引）
        elif env_type == "windows":
            print("\n✅ Windows 需手动安装，步骤如下：")
            print("1. 访问 https://www.python.org/downloads/windows/")
            print("2. 下载最新版，安装时勾选「Add Python to PATH」")
            print("3. 安装后在 cmd 输入 python --version 验证")

        # 3. macOS 环境（用 brew 安装）
        elif env_type == "macos":
            print("\n[1/2] 检查 Homebrew...")
            try:
                subprocess.run(["brew", "--version"], check=True, stdout=subprocess.DEVNULL)
            except FileNotFoundError:
                subprocess.run('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"', shell=True, check=True)
            print("[2/2] 安装 Python...")
            subprocess.run(["brew", "install", "python"], check=True, stdout=subprocess.DEVNULL)
            py_ver = subprocess.run(["python3", "--version"], stdout=subprocess.PIPE, text=True).stdout.strip()
            pip_ver = subprocess.run(["pip3", "--version"], stdout=subprocess.PIPE, text=True).stdout.strip()
            print(f"\n🎉 安装成功！Python3：{py_ver}\npip3：{pip_ver}")

        # 4. 常规 Linux 环境（用 apt/yum，自动适配）
        elif env_type == "linux":
            print("\n[1/2] 安装 Python3...")
            try:
                subprocess.run(["sudo", "apt", "update"], check=True, stdout=subprocess.DEVNULL)
                subprocess.run(["sudo", "apt", "install", "python3", "python3-pip", "-y"], check=True, stdout=subprocess.DEVNULL)
            except FileNotFoundError:
                subprocess.run(["sudo", "yum", "update", "-y"], check=True, stdout=subprocess.DEVNULL)
                subprocess.run(["sudo", "yum", "install", "python3", "python3-pip", "-y"], check=True, stdout=subprocess.DEVNULL)
            py_ver = subprocess.run(["python3", "--version"], stdout=subprocess.PIPE, text=True).stdout.strip()
            pip_ver = subprocess.run(["pip3", "--version"], stdout=subprocess.PIPE, text=True).stdout.strip()
            print(f"\n🎉 安装成功！Python3：{py_ver}\npip3：{pip_ver}")

        # 未知环境
        else:
            print("\n❌ 不支持当前未知环境，请手动安装 Python！")
            sys.exit(1)

    except subprocess.CalledProcessError as e:
        print(f"\n❌ 安装失败！错误详情：{e.stderr[:300]}")
        sys.exit(1)

if __name__ == "__main__":
    install_python()
