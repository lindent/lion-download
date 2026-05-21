@echo off
chcp 65001 >nul
color 0A
echo.
echo  ███████╗██╗   ██╗███╗   ███╗██████╗  ██████╗ ███████╗██████╗ 
echo  ██╔════╝╚██╗ ██╔╝████╗ ████║██╔══██╗██╔═══██╗██╔════╝██╔══██╗
echo  ███████╗ ╚████╔╝ ██╔████╔██║██████╔╝██║   ██║███████╗██████╔╝
echo  ╚════██║  ╚██╔╝  ██║╚██╔╝██║██╔═══╝ ██║   ██║╚════██║██╔══██╗
echo  ███████║   ██║   ██║ ╚═╝ ██║██║     ╚██████╔╝███████║██║  ██║
echo  ╚══════╝   ╚═╝   ╚═╝     ╚═╝╚═╝      ╚═════╝ ╚══════╝╚═╝  ╚═╝
echo.
echo ================================================================
echo              Temu 图片下载工具 - 智能打包系统 v1.0
echo ================================================================
echo.
echo [提示] 本脚本将自动完成以下工作：
echo   1. 检查系统环境
echo   2. 安装必要组件
echo   3. 打包生成 exe 文件
echo   4. 创建可直接交付的文件夹
echo.
echo ================================================================
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] 建议以管理员身份运行，以避免权限问题
    echo.
)

REM 检查Python
echo [步骤 1/4] 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python！
    echo.
    echo 请先安装Python 3.8或更高版本：
    echo   1. 打开网址: https://www.python.org/downloads/
    echo   2. 下载最新版本的Python (3.x)
    echo   3. 运行安装程序
    echo   4. 【重要】勾选 "Add Python to PATH"
    echo   5. 点击 "Install Now"
    echo.
    pause
    start https://www.python.org/downloads/
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo   ✓ %PYTHON_VERSION%
echo.

REM 安装PyInstaller
echo [步骤 2/4] 检查/安装打包工具...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo   正在安装 PyInstaller...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo [错误] PyInstaller 安装失败！
        pause
        exit /b 1
    )
) else (
    echo   ✓ PyInstaller 已安装
)
echo.

REM 清理旧构建
echo [步骤 3/4] 清理旧构建文件...
if exist "build" (
    rmdir /s /q "build"
    echo   ✓ 已清理 build 目录
)
if exist "dist" (
    rmdir /s /q "dist"
    echo   ✓ 已清理 dist 目录
)
echo.

REM 执行打包
echo [步骤 4/4] 开始打包应用程序...
echo   这可能需要几分钟时间，请耐心等待...
echo.

pyinstaller temu_downloader.spec --clean

if %errorlevel% neq 0 (
    echo.
    echo [错误] 打包过程出现错误！
    pause
    exit /b 1
)

echo.
echo ================================================================
echo                      打包成功完成！
echo ================================================================
echo.
echo [成功] 您的可执行文件已生成：
echo.
echo   📦 位置: dist\TemuDownloader\TemuDownloader.exe
echo.
echo [下一步操作]
echo   1. 将 "dist\TemuDownloader" 文件夹复制到目标电脑
echo   2. 无需安装Python或其他依赖
echo   3. 直接双击 "TemuDownloader.exe" 即可运行
echo.
echo [交付清单]
echo   ✓ TemuDownloader.exe  (主程序)
echo   ✓ Python运行时库     (已打包)
echo   ✓ 所有依赖文件       (已打包)
echo.
echo ================================================================
echo.

REM 打开输出目录
explorer "dist\TemuDownloader"

pause
