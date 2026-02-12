@echo off
title FNF Ultimate Chrono Bot Launcher

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    pause
    exit /b
)

:menu
cls
python fnf_bot.py
:: If we reach here, it means the bot exited.
:: To avoid "Terminate batch job" we use this trick:
exit
