set TBED=C:\_LDRA_Toolsuite\1002_RC3
set WORK=C:\_LDRA_Workarea\1002_RC3
set PYTHON_PATH=%TBED%\Utils\Python
set PATH=%PYTHON_PATH%;%TBED%;%PATH%

set TRIMMER=%TBED%\Utils\Tcf_trimmer\tcf_trimmer.py
set TCF_FOLDER=%WORK%\Examples\Toolsuite\Cashregister_6.0\LowLevelTests

python.exe %TRIMMER% %TCF_FOLDER%
