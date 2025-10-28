#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para DELETAR os campos c_inicial e c_final do shapefile
para que possamos recriar do zero.
"""

import sys
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from qgis.core import (
    QgsApplication,
    QgsVectorLayer
)

def deletar_campos(caminho_shapefile):
    """Deleta os campos c_inicial e c_final."""
    
    print("="*70)
    print("🗑️  DELETAR CAMPOS")
    print("="*70)
    
    layer = QgsVectorLayer(caminho_shapefile, "test", "ogr")
    
    if not layer.isValid():
        print("❌ ERRO: Shapefile inválido!")
        return False
    
    print(f"\n📁 Shapefile: {caminho_shapefile}")
    
    # Verificar campos
    field_names = [field.name() for field in layer.fields()]
    print(f"   Campos atuais: {field_names}")
    
    # Iniciar edição
    if not layer.startEditing():
        print("❌ ERRO: Não foi possível iniciar edição!")
        return False
    
    # Deletar campos se existirem
    campos_deletados = []
    
    if 'c_inicial' in field_names:
        idx = layer.fields().indexOf('c_inicial')
        if layer.deleteAttribute(idx):
            campos_deletados.append('c_inicial')
            print(f"   ✅ Campo 'c_inicial' deletado!")
    
    if 'c_final' in field_names:
        idx = layer.fields().indexOf('c_final')
        if layer.deleteAttribute(idx):
            campos_deletados.append('c_final')
            print(f"   ✅ Campo 'c_final' deletado!")
    
    # Atualizar campos
    layer.updateFields()
    
    # Salvar
    print("\n💾 Salvando alterações...")
    if layer.commitChanges():
        print("✅ Campos deletados com sucesso!")
        print(f"   Campos removidos: {campos_deletados}")
        return True
    else:
        print("❌ ERRO ao salvar:")
        for error in layer.commitErrors():
            print(f"   - {error}")
        layer.rollBack()
        return False


def main():
    """Função principal."""
    
    QgsApplication.setPrefixPath("C:/Program Files/QGIS*", True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    
    try:
        if len(sys.argv) < 2:
            print("Uso: python deletar_campos.py <caminho_shapefile>")
            return 1
        
        sucesso = deletar_campos(sys.argv[1])
        return 0 if sucesso else 1
    
    finally:
        qgs.exitQgis()


if __name__ == "__main__":
    sys.exit(main())
