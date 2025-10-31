@echo off
REM SitePanda Desktop - Windows Desktop Shortcut Creator

echo Creating desktop shortcut for SitePanda Desktop...

REM Get the directory where this script is located
set APP_DIR=%~dp0
set APP_PATH=%APP_DIR%app.py

REM Create VBS script to create shortcut
set VBS_SCRIPT=%TEMP%\create_shortcut.vbs
echo Set oWS = WScript.CreateObject("WScript.Shell") > %VBS_SCRIPT%
echo sLinkFile = "%USERPROFILE%\Desktop\SitePanda Desktop.lnk" >> %VBS_SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %VBS_SCRIPT%
echo oLink.TargetPath = "python" >> %VBS_SCRIPT%
echo oLink.Arguments = """%APP_PATH%""" >> %VBS_SCRIPT%
echo oLink.WorkingDirectory = "%APP_DIR%" >> %VBS_SCRIPT%
echo oLink.Description = "SitePanda Desktop - Manage Duda Sites" >> %VBS_SCRIPT%
echo oLink.IconLocation = "%APP_DIR%assets\icon.ico" >> %VBS_SCRIPT%
echo oLink.Save >> %VBS_SCRIPT%

REM Execute the VBS script
cscript //nologo %VBS_SCRIPT%

REM Clean up
del %VBS_SCRIPT%

REM Also create Start Menu shortcut
set START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs
if not exist "%START_MENU%" mkdir "%START_MENU%"

set VBS_SCRIPT2=%TEMP%\create_shortcut2.vbs
echo Set oWS = WScript.CreateObject("WScript.Shell") > %VBS_SCRIPT2%
echo sLinkFile = "%START_MENU%\SitePanda Desktop.lnk" >> %VBS_SCRIPT2%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %VBS_SCRIPT2%
echo oLink.TargetPath = "python" >> %VBS_SCRIPT2%
echo oLink.Arguments = """%APP_PATH%""" >> %VBS_SCRIPT2%
echo oLink.WorkingDirectory = "%APP_DIR%" >> %VBS_SCRIPT2%
echo oLink.Description = "SitePanda Desktop - Manage Duda Sites" >> %VBS_SCRIPT2%
echo oLink.IconLocation = "%APP_DIR%assets\icon.ico" >> %VBS_SCRIPT2%
echo oLink.Save >> %VBS_SCRIPT2%

cscript //nologo %VBS_SCRIPT2%
del %VBS_SCRIPT2%

echo.
echo Desktop shortcut created successfully!
echo.
echo You can now find 'SitePanda Desktop' on your:
echo   - Desktop
echo   - Start Menu
echo.
pause
