@echo off
REM ============================================
REM Script para executar consulta standalone
REM ============================================

title Consulta Standalone - PyQGIS

REM Caminho do QGIS
set QGIS_PATH=C:\Program Files\QGIS 3.12

REM Verificar se QGIS existe
if not exist "%QGIS_PATH%\bin\python-qgis.bat" (
    echo [ERRO] QGIS nao encontrado em: %QGIS_PATH%
    pause
    exit /b 1
)

echo.
echo ========================================
echo   CONSULTA STANDALONE - PyQGIS
echo ========================================
echo.

REM Verificar argumentos
if "%~1"=="" (
    echo USO:
    echo   %~nx0 X Y ZONA
    echo.
    echo EXEMPLO:
    echo   %~nx0 510807 8649627 24
    echo.
    echo OU execute com parametros:
    echo   executar_standalone.bat 510807 8649627 24
    echo.
    pause
    exit /b 1
)

set X=%~1
set Y=%~2
set ZONA=%~3

if "%ZONA%"=="" (
    echo [ERRO] Faltam parametros!
    echo.
    echo USO: %~nx0 X Y ZONA
    echo EXEMPLO: %~nx0 510807 8649627 24
    echo.
    pause
    exit /b 1
)

echo Coordenadas:
echo   X:    %X%
echo   Y:    %Y%
echo   Zona: %ZONA%
echo.
echo Executando consulta...
echo.

REM Executar com Python do QGIS
"%QGIS_PATH%\bin\python-qgis.bat" consulta_standalone.py --x %X% --y %Y% --zona %ZONA%

echo.
pause
