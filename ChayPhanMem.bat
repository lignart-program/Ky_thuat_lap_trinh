@echo off
chcp 65001 > nul
cd /d "%~dp0"
title Hệ Thống Quản Lý Dự Án
color F0
echo Đang khởi động hệ thống...
python "code.py"
pause
