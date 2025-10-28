@echo off
REM ============================================
REM Script para extrair coordenadas inicio/fim
REM ============================================

title Extrator de Coordenadas - Rodovias Federais

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
echo   EXTRATOR DE COORDENADAS
echo   Rodovias Federais
echo ========================================
echo.

REM Caminho do shapefile
set SHAPEFILE=C:\Users\savio\OneDrive\Documentos\repositories\ConsultaCoordenadasSIT\shapes\shapesFederais_07-2025.shp

echo Shapefile: %SHAPEFILE%
echo.

REM Verificar se o shapefile existe
if not exist "%SHAPEFILE%" (
    echo [ERRO] Shapefile nao encontrado!
    echo   Caminho: %SHAPEFILE%
    echo.
    pause
    exit /b 1
)

echo Executando extracao de coordenadas...
echo.

REM Executar com Python do QGIS
"%PYTHON_QGIS%" extrair_coordenadas_standalone.py "%SHAPEFILE%"

echo.
echo ========================================
echo   Operacao concluida!
echo ========================================
echo.
pause
