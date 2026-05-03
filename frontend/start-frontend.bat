@echo off
chcp 65001 >nul
echo ====================================
echo 种植周期管理系统 - 前端服务启动
echo ====================================
echo.

cd /d "%~dp0"

echo [%date% %time%] 正在启动前端服务...
echo 前端将在 http://localhost:5173 运行
echo 按 Ctrl+C 可以停止服务
echo.

REM 设置环境变量，确保使用IPv4
set NODE_OPTIONS=--ipv4

REM 启动前端服务
npm run dev

echo.
echo [%date% %time%] 前端服务已停止
pause
