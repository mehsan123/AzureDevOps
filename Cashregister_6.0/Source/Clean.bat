if exist inszt_*.c del /F inszt_*.c
if exist *.cerr del /F *.cerr
if exist *.o del /F *.o
if exist *.d del /F *.d
if exist *.exh del /F *.exh
if exist *.txt del /F *.txt
if exist *.exe.btf del /F *.exe.btf
if exist Cashregister.exe del /F Cashregister.exe

if errorlevel 1 pause
