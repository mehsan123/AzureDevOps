
@echo off
rem +---------------------------------------------------------+
rem | Author : M.W.Richardson                                 |
rem | Date   : 10/08/2020                                     |
rem |                                                         |
rem | Uses the GLHAPI to get all results and print them in    |
rem | XML format                                              |
rem |                                                         |
rem | Copyright : (c) 2020 Liverpool Data Research Associates |
rem +---------------------------------------------------------+

set TBED=C:\_LDRA_Toolsuite\1002_RC3
set WORK=C:\_LDRA_Workarea\1002_RC3
set PRJ=Cashregister

if exist "%TBED%\TBbrowse.exe" (
  set GLH_FILE=%WORK%\%PRJ%_tbwrkfls\%PRJ%.glh
) else (
  set GLH_FILE=%WORK%\%PRJ%_tbwrkfls\%PRJ%.ldra
)

set XML_FILE=%WORK%\%PRJ%_tbwrkfls\%PRJ%.xml

copy %WORK%\Examples\Workshops\Generate_xml\Release\Generate_xml.exe %TBED%\Generate_xml.exe
@echo on
%TBED%\Generate_xml.exe %GLH_FILE%
@echo off

if exist %XML_FILE% %XML_FILE%
