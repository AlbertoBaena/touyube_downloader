@echo off

cd /d "%~dp0mp3_downloads"

adb push . /sdcard/Music/
del /q *

echo.
echo Files copied succesfully.
pause