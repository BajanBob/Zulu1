@echo off
title Zulu 1 Tutor Bubba
set "HTML=%~dp0app\index.html"
for /f "delims=" %%u in ('powershell -NoProfile -Command "([System.Uri]$env:HTML).AbsoluteUri"') do set "URL=%%u"
start "" msedge --app="%URL%" --window-size=1100,850
if errorlevel 1 start "" "%HTML%"
exit
