@echo off

REM Read the commands from setup.txt and execute them line by line
for /F "usebackq tokens=* delims=" %%i in (setup.txt) do (
    %%i
)

REM Launch the web browser to open the application
start http://127.0.0.1:5000/
