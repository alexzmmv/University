
echo off
COLOR 0A
echo creating obj files...
timeout /t 2 /nobreak >nul

.\nasm -fobj func.asm
.\nasm -fobj main.asm

echo obj files created
echo linkinkg...
.\alink.exe main.obj func.obj -oPE -subsys console -entry start

pause

color 0F
.\main.exe