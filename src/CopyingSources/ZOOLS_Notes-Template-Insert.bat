@echo off
cd %~dp0                     
set "scriptPath=src/Zools/ZOOLS_Notes-Template-Insert.ps1"       

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Start-Process powershell.exe -ArgumentList '-WindowStyle Hidden -NoProfile -ExecutionPolicy Bypass -File ""%cd%\%scriptPath%""' -Verb RunAs"
