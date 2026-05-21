@echo off
chcp 65001 >nul
echo ==========================================
echo   Temu 图片下载工具 - 打包脚本
echo ==========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 安装PyInstaller
echo [1/3] 检查并安装 PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 正在安装 PyInstaller...
    pip install pyinstaller
) else (
    echo PyInstaller 已安装
)

REM 清理旧构建
echo [2/3] 清理旧构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM 执行打包
echo [3/3] 开始打包...
echo.
pyinstaller temu_downloader.spec --clean

echo.
echo ==========================================
echo   打包完成！
echo ==========================================
echo.
echo 可执行文件位置: dist\TemuDownloader\TemuDownloader.exe
echo.
pause
