@echo off

echo Installing Kat to %APPDATA%\Kat...
powershell -Command "Invoke-WebRequest https://github.com/Duckapple/Kat/archive/refs/heads/master.zip -OutFile kat.zip"
powershell Expand-Archive kat.zip -DestinationPath %APPDATA%
move %APPDATA%\Kat-master %APPDATA%\Kat

echo Installing Python dependencies...
python -m pip install --user -r %APPDATA%\Kat\requirements.txt

@REM env setup from <https://stackoverflow.com/questions/43934167/how-to-get-only-the-user-path-variable>
setlocal EnableExtensions DisableDelayedExpansion
set "UserPath="
for /F "skip=2 tokens=1,2*" %%G in ('%SystemRoot%\System32\reg.exe query "HKCU\Environment" /v "Path" 2^>nul') do if /I "%%G" == "Path" (
    if /I "%%H" == "REG_EXPAND_SZ" (call set "UserPath=%%I") else if /I "%%H" == "REG_SZ" set "UserPath=%%I"
    if defined UserPath goto UserPathRead
)

:UserPathRead
setlocal EnableDelayedExpansion
setx Path "!UserPath!;%APPDATA%\Kat"
endlocal

echo Kat installed!
echo Install location: %APPDATA%\Kat
echo Invoke via 'kattis' (runs the 'kattis.bat' in the install directory)
echo Continue to open site for downloading Kattis credentials/config
pause

echo Opening browser (https://open.kattis.com/download/kattisrc)...
start https://open.kattis.com/download/kattisrc
echo Please save to your user directory as '.kattisrc'
pause

echo "Thanks for installing!"
:EndLabel
