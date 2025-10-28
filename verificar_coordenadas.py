#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar as coordenadas armazenadas no shapefile.
"""

import sys
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from qgis.core import (
    QgsApplication,
    QgsVectorLayer
)

def verificar_coordenadas(caminho_shapefile):
    """Verifica as primeiras 5 feições do shapefile."""
    
    print("="*70)
    print("🔍 VERIFICADOR DE COORDENADAS")
    print("="*70)
    
    # Carregar shapefile
    layer = QgsVectorLayer(caminho_shapefile, "test", "ogr")
    
    if not layer.isValid():
        print("❌ ERRO: Shapefile inválido!")
        return False
    
    print(f"\n📁 Shapefile: {caminho_shapefile}")
    print(f"📍 CRS: {layer.crs().authid()} - {layer.crs().description()}")
    print(f"📊 Total de feições: {layer.featureCount()}")
    
    # Verificar campos
    field_names = [field.name() for field in layer.fields()]
    
    if 'c_inicial' not in field_names or 'c_final' not in field_names:
        print("\n❌ Campos 'c_inicial' e 'c_final' não encontrados!")
        print(f"   Campos disponíveis: {field_names}")
        return False
    
    print("\n" + "="*70)
    print("📋 PRIMEIRAS 5 FEIÇÕES:")
    print("="*70)
    
    # Mostrar primeiras 5 feições
    for i, feature in enumerate(layer.getFeatures()):
        if i >= 5:
            break
        
        geom = feature.geometry()
        c_inicial = feature['c_inicial']
        c_final = feature['c_final']
        
        # Pegar coordenadas originais
        if geom.isMultipart():
            lines = geom.asMultiPolyline()
            first_line = lines[0]
            last_line = lines[-1]
            ponto_orig_inicial = first_line[0]
            ponto_orig_final = last_line[-1]
        else:
            line = geom.asPolyline()
            ponto_orig_inicial = line[0]
            ponto_orig_final = line[-1]
        
        print(f"\n🔹 Feição {i+1} (ID: {feature.id()}):")
        print(f"   Geometria Original (EPSG:{layer.crs().authid()}):")
        print(f"      Início: X={ponto_orig_inicial.x():.6f}, Y={ponto_orig_inicial.y():.6f}")
        print(f"      Fim:    X={ponto_orig_final.x():.6f}, Y={ponto_orig_final.y():.6f}")
        print(f"   Campos de Atributos:")
        print(f"      c_inicial: {c_inicial}")
        print(f"      c_final:   {c_final}")
    
    print("\n" + "="*70)
    return True


def main():
    """Função principal."""
    
    QgsApplication.setPrefixPath("C:/Program Files/QGIS*", True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    
    try:
        if len(sys.argv) < 2:
            print("Uso: python verificar_coordenadas.py <caminho_shapefile>")
            return 1
        
        sucesso = verificar_coordenadas(sys.argv[1])
        return 0 if sucesso else 1
    
    finally:
        qgs.exitQgis()


if __name__ == "__main__":
    sys.exit(main())
