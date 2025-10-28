@echo off
REM ============================================
REM Script para executar consulta standalone
REM ============================================

title Consulta Standalone - PyQGIS

REM Detectar versao do QGIS automaticamente
set QGIS_PATH=
set PYTHON_QGIS=

REM Procurar QGIS em Program Files
if exist "C:\Program Files\" (
    for /f "delims=" %%i in ('dir "C:\Program Files\QGIS*" /b /ad 2^>nul') do (
        REM Tentar encontrar o arquivo python do QGIS (varias versoes possiveis)
        if exist "C:\Program Files\%%i\bin\python-qgis-ltr.bat" (
            set "QGIS_PATH=C:\Program Files\%%i"
            set "PYTHON_QGIS=C:\Program Files\%%i\bin\python-qgis-ltr.bat"
            goto :qgis_found
        )
        if exist "C:\Program Files\%%i\bin\python-qgis.bat" (
            set "QGIS_PATH=C:\Program Files\%%i"
            set "PYTHON_QGIS=C:\Program Files\%%i\bin\python-qgis.bat"
            goto :qgis_found
        )
        if exist "C:\Program Files\%%i\bin\python3.exe" (
            set "QGIS_PATH=C:\Program Files\%%i"
            set "PYTHON_QGIS=C:\Program Files\%%i\bin\python3.exe"
            goto :qgis_found
        )
    )
)

REM Procurar QGIS em Program Files (x86)
if exist "C:\Program Files (x86)\" (
    for /f "delims=" %%i in ('dir "C:\Program Files (x86)\QGIS*" /b /ad 2^>nul') do (
        REM Tentar encontrar o arquivo python do QGIS (varias versoes possiveis)
        if exist "C:\Program Files (x86)\%%i\bin\python-qgis-ltr.bat" (
            set "QGIS_PATH=C:\Program Files (x86)\%%i"
            set "PYTHON_QGIS=C:\Program Files (x86)\%%i\bin\python-qgis-ltr.bat"
            goto :qgis_found
        )
        if exist "C:\Program Files (x86)\%%i\bin\python-qgis.bat" (
            set "QGIS_PATH=C:\Program Files (x86)\%%i"
            set "PYTHON_QGIS=C:\Program Files (x86)\%%i\bin\python-qgis.bat"
            goto :qgis_found
        )
        if exist "C:\Program Files (x86)\%%i\bin\python3.exe" (
            set "QGIS_PATH=C:\Program Files (x86)\%%i"
            set "PYTHON_QGIS=C:\Program Files (x86)\%%i\bin\python3.exe"
            goto :qgis_found
        )
    )
)

REM QGIS nao encontrado
echo [ERRO] QGIS nao encontrado!
echo.
echo O QGIS deve estar instalado em:
echo   - C:\Program Files\QGIS*
echo   - C:\Program Files (x86)\QGIS*
echo.
echo Verifique se o QGIS esta instalado corretamente.
echo.
pause
exit /b 1

:qgis_found
echo [INFO] QGIS encontrado em: %QGIS_PATH%
echo [INFO] Python QGIS: %PYTHON_QGIS%
echo.

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
"%PYTHON_QGIS%" consulta_standalone.py --x %X% --y %Y% --zona %ZONA%

echo.
pause
