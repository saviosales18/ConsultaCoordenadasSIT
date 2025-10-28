@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

REM ========================================================================
REM Script para extrair coordenadas de rodovias estaduais
REM ========================================================================

set "PYTHON_QGIS="
set "SHAPEFILE=%~dp0shapes\shapesEstaduais_04-2024.shp"

REM Detectar QGIS
echo [INFO] Procurando instalação do QGIS...
for /f "delims=" %%i in ('dir "C:\Program Files\QGIS*" /b /ad 2^>nul') do (
    set "QGIS_DIR=C:\Program Files\%%i"
    echo [INFO] QGIS encontrado em: !QGIS_DIR!
    
    REM Verificar python-qgis-ltr.bat primeiro
    if exist "!QGIS_DIR!\bin\python-qgis-ltr.bat" (
        set "PYTHON_QGIS=!QGIS_DIR!\bin\python-qgis-ltr.bat"
        echo [INFO] Python QGIS: !PYTHON_QGIS!
        goto :found_qgis
    )
    
    REM Verificar python-qgis.bat
    if exist "!QGIS_DIR!\bin\python-qgis.bat" (
        set "PYTHON_QGIS=!QGIS_DIR!\bin\python-qgis.bat"
        echo [INFO] Python QGIS: !PYTHON_QGIS!
        goto :found_qgis
    )
    
    REM Verificar python3.exe
    if exist "!QGIS_DIR!\bin\python3.exe" (
        set "PYTHON_QGIS=!QGIS_DIR!\bin\python3.exe"
        echo [INFO] Python QGIS: !PYTHON_QGIS!
        goto :found_qgis
    )
)

echo [ERRO] QGIS não encontrado!
pause
exit /b 1

:found_qgis

REM Executar script Python
echo.
echo ========================================================================
echo Executando extração de coordenadas - RODOVIAS ESTADUAIS
echo ========================================================================
call "!PYTHON_QGIS!" "%~dp0extrair_coordenadas_standalone.py" "%SHAPEFILE%"

echo.
echo ========================================================================
pause
