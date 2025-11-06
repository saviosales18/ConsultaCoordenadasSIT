@echo off
REM ============================================
REM Script para compilar o executavel
REM Execute como ADMINISTRADOR
REM ============================================

title Compilando Consulta de Coordenadas

echo ============================================================================
echo   COMPILADOR - CONSULTA DE COORDENADAS
echo ============================================================================
echo.

REM Verificar se esta rodando como administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERRO] Este script precisa ser executado como ADMINISTRADOR!
    echo.
    echo Clique com botao direito e selecione "Executar como administrador"
    echo.
    pause
    exit /b 1
)

echo [INFO] Executando como administrador... OK
echo.

REM Caminho do Python do QGIS
set PYTHON_QGIS=C:\Program Files\QGIS 3.12\bin\python-qgis.bat

if not exist "%PYTHON_QGIS%" (
    echo [ERRO] Python do QGIS nao encontrado!
    echo Caminho esperado: %PYTHON_QGIS%
    echo.
    pause
    exit /b 1
)

echo [INFO] Python QGIS encontrado: %PYTHON_QGIS%
echo.

REM 1. Instalar PyInstaller
echo [PASSO 1/2] Instalando PyInstaller...
echo.
"%PYTHON_QGIS%" -m pip install pyinstaller --quiet
if %errorLevel% neq 0 (
    echo [ERRO] Falha ao instalar PyInstaller
    pause
    exit /b 1
)
echo [OK] PyInstaller instalado com sucesso
echo.

REM 2. Compilar executavel
echo [PASSO 2/2] Compilando executavel...
echo.
"%PYTHON_QGIS%" build_exe.py
if %errorLevel% neq 0 (
    echo [ERRO] Falha na compilacao
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo   COMPILACAO CONCLUIDA!
echo ============================================================================
echo.
echo O executavel foi gerado em:
echo   dist\Consulta de Coordenadas.exe
echo.
echo Para distribuir, copie junto:
echo   - Consulta de Coordenadas.exe
echo   - LARGURAS FXD\ (pasta completa)
echo.
pause
