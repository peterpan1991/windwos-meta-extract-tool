@echo off
chcp 65001 > nul
title DJYMeta - 元数据提取工具

echo ========================================
echo   DJYMeta - 元数据提取工具
echo ========================================
echo.

REM 检查 Python 是否安装
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python，请先安装 Python 3.8 或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [信息] 正在启动 GUI 界面...
echo.

REM 运行 GUI
python run_gui.py

if %errorlevel% neq 0 (
    echo.
    echo [错误] 程序运行失败
    pause
    exit /b 1
)
