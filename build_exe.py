#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para compilar o executável standalone com PyInstaller.
Inclui todas as dependências do QGIS.

Uso:
    python build_exe.py
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Compila o executável com PyInstaller."""
    
    print("=" * 76)
    print("  COMPILADOR - CONSULTA DE COORDENADAS")
    print("=" * 76)
    print()
    
    # Verificar se PyInstaller está instalado
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado:", PyInstaller.__version__)
    except ImportError:
        print("❌ PyInstaller não encontrado!")
        print()
        print("Instale com:")
        print("  pip install pyinstaller")
        print()
        return 1
    
    # Verificar se QGIS está disponível
    qgis_path = r"C:\Program Files\QGIS 3.12"
    if not os.path.exists(qgis_path):
        print(f"❌ QGIS não encontrado em: {qgis_path}")
        print()
        print("Ajuste o caminho do QGIS no script build_exe.py")
        return 1
    
    print(f"✅ QGIS encontrado: {qgis_path}")
    print()
    
    # Configurar variáveis de ambiente para o QGIS
    qgis_bin = os.path.join(qgis_path, "bin")
    qgis_python = os.path.join(qgis_path, "apps", "Python39")
    qgis_plugins = os.path.join(qgis_python, "Lib", "site-packages")
    
    # Adicionar ao PATH
    os.environ["PATH"] = f"{qgis_bin};{os.environ.get('PATH', '')}"
    os.environ["PYTHONPATH"] = f"{qgis_plugins};{os.environ.get('PYTHONPATH', '')}"
    
    # Comando PyInstaller
    comando = [
        "pyinstaller",
        "--onefile",  # Gerar um único executável
        "--console",  # Aplicação console
        "--name=Consulta de Coordenadas",  # Nome do executável
        "--icon=NONE",  # Sem ícone (pode adicionar depois)
        
        # Incluir dados necessários
        "--add-data=LARGURAS FXD;LARGURAS FXD",
        
        # Caminhos do QGIS
        f"--paths={qgis_plugins}",
        f"--paths={qgis_bin}",
        
        # Hidden imports (módulos não detectados automaticamente)
        "--hidden-import=qgis.core",
        "--hidden-import=qgis.analysis",
        "--hidden-import=qgis.gui",
        "--hidden-import=qgis._core",
        "--hidden-import=qgis._analysis",
        "--hidden-import=PyQt5",
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=PyQt5.QtWidgets",
        
        # Coletar DLLs do QGIS
        f"--collect-all=qgis",
        
        # Arquivo principal
        "consulta_interativa.py"
    ]
    
    print("🔧 Iniciando compilação...")
    print()
    print("Comando:")
    print(" ".join(comando))
    print()
    print("-" * 76)
    print()
    
    try:
        # Executar PyInstaller
        resultado = subprocess.run(comando, check=True)
        
        print()
        print("-" * 76)
        print()
        print("✅ COMPILAÇÃO CONCLUÍDA!")
        print()
        print("Executável gerado em:")
        print(f"  {Path('dist').resolve()}\\Consulta de Coordenadas.exe")
        print()
        print("⚠️  IMPORTANTE:")
        print("  1. Copie a pasta 'LARGURAS FXD' para o mesmo diretório do .exe")
        print("  2. O executável incluirá as DLLs do QGIS automaticamente")
        print()
        
        return 0
    
    except subprocess.CalledProcessError as e:
        print()
        print("-" * 76)
        print()
        print(f"❌ ERRO na compilação: {e}")
        print()
        return 1
    
    except Exception as e:
        print()
        print(f"❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
