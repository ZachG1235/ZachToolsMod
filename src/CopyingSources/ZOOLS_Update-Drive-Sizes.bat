@echo off
setlocal EnableDelayedExpansion

set "URL=REPLACE-HERE-WITH-URL"
set "DRIVELIST=%~dp0src\Zools\Drive_Names.txt"

if not exist "%DRIVELIST%" (
    echo Could not find %DRIVELIST%
    pause
    exit /b 1
)

set "NAMES="
for /f "usebackq delims=" %%L in ("%DRIVELIST%") do (
    if defined NAMES (set "NAMES=!NAMES!, %%L") else (set "NAMES=%%L")
)
echo Names in drives.txt: %NAMES%
echo.
echo Drives detected:

for /f "usebackq tokens=1-3 delims=|" %%A in (`powershell -NoProfile -Command "Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=2 OR DriveType=3' | Where-Object { $_.VolumeName -and $_.DeviceID -ne $env:SystemDrive } | ForEach-Object { '{0}|{1}|{2}' -f $_.VolumeName, [math]::Round($_.FreeSpace/1GB,2), [math]::Round($_.Size/1GB,2) }"`) do call :check "%%A" "%%B" "%%C"

echo.
echo Done.
pause
exit /b

:check
set "KEY=%~1"
set "VALUE=%~2"
set "SIZE=%~3"
echo Checking [%KEY%] - %VALUE% GB free of %SIZE% GB total

findstr /x /i /l /c:"%KEY%" "%DRIVELIST%" >nul
if errorlevel 1 (
    echo   not found in drives.txt
    exit /b
)

echo   MATCH - sending
curl -L "%URL%" -H "Content-Type: application/json" -d "{\"key\":\"%KEY%\",\"value\":\"%VALUE%\",\"size\":\"%SIZE%\"}"
echo.
exit /b