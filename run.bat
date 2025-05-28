@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo 正在安装依赖...
pip install -r requirements.txt --no-cache-dir

if %errorlevel% neq 0 (
    echo  依赖安装失败，请检查网络或 requirements.txt
    pause
    exit /b
)

echo.
echo  正在启动程序...
python main.py

echo.
echo  程序已退出。
pause现在在cmd里还是不显示图标