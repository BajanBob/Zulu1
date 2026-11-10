@echo off
title Install Zulu 1 Tutor Bubba
set "HTML=%~dp0app\index.html"
set "ICO=%~dp0app\zulu1.ico"
echo Adding Zulu 1 Tutor Bubba to the Desktop and Start Menu...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$e=(Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe' -ErrorAction SilentlyContinue).'(default)'; if(-not $e){$e=Join-Path ${env:ProgramFiles(x86)} 'Microsoft\Edge\Application\msedge.exe'}; $u=([System.Uri]$env:HTML).AbsoluteUri; $s=New-Object -ComObject WScript.Shell; foreach($d in @([Environment]::GetFolderPath('Desktop'), (Join-Path ([Environment]::GetFolderPath('StartMenu')) 'Programs'))){ $l=$s.CreateShortcut((Join-Path $d 'Zulu 1 Tutor Bubba.lnk')); $l.TargetPath=$e; $l.Arguments='--app=' + [char]34 + $u + [char]34 + ' --window-size=1100,850'; $l.IconLocation=$env:ICO; $l.Description='Zulu 1 Tutor Bubba for Master Bubba'; $l.Save() }"
echo.
echo Done! Look for the "Zulu 1 Tutor Bubba" puppy icon on the Desktop.
echo Keep this folder where it is. The shortcut opens the app from here.
pause
