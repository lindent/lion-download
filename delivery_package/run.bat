@echo off
chcp 65001 >nul
echo ==========================================
echo   Temu 图片下载工具
echo ==========================================
echo.
python temu_downloader.py
if errorlevel 1 (
    echo.
    echo [错误] 程序运行失败
    pause
)
