#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simples de conversão de coordenadas.
"""

import sys
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from qgis.core import (
    QgsApplication,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
    QgsPointXY
)

def teste_conversao():
    """Testa a conversão de um ponto de SIRGAS 2000 (lat/lon) para UTM."""
    
    print("="*70)
    print("🧪 TESTE DE CONVERSÃO DE COORDENADAS")
    print("="*70)
    
    # Ponto de teste (primeira feição do shapefile)
    lon = -46.197733
    lat = -13.956491
    
    print(f"\n📍 Ponto Original:")
    print(f"   Longitude: {lon}°")
    print(f"   Latitude: {lat}°")
    print(f"   CRS: SIRGAS 2000 (EPSG:4674)")
    
    # Calcular zona UTM
    zona = int((lon + 180) / 6) + 1
    print(f"\n🗺️  Zona UTM Calculada: {zona}")
    
    # SIRGAS 2000 / UTM zone ##S
    # Zona 18S = EPSG:31978
    # Zona 19S = EPSG:31979
    # Zona 20S = EPSG:31980
    # Zona 21S = EPSG:31981
    # Zona 22S = EPSG:31982
    # Zona 23S = EPSG:31983
    # Zona 24S = EPSG:31984
    # Zona 25S = EPSG:31985
    #
    # Fórmula: EPSG = 31960 + zona
    epsg_utm = 31960 + zona
    print(f"   EPSG UTM: {epsg_utm}")
    
    # Criar CRS
    crs_origem = QgsCoordinateReferenceSystem("EPSG:4674")  # SIRGAS 2000
    crs_wgs84 = QgsCoordinateReferenceSystem("EPSG:4326")   # WGS84
    crs_utm = QgsCoordinateReferenceSystem(f"EPSG:{epsg_utm}")  # SIRGAS 2000 UTM
    
    print(f"\n🔄 Conversões:")
    print(f"   Origem: {crs_origem.authid()} - {crs_origem.description()}")
    print(f"   WGS84: {crs_wgs84.authid()} - {crs_wgs84.description()}")
    print(f"   Destino UTM: {crs_utm.authid()} - {crs_utm.description()}")
    
    # Criar ponto
    ponto = QgsPointXY(lon, lat)
    
    # Conversão 1: SIRGAS 2000 -> WGS84
    trans1 = QgsCoordinateTransform(crs_origem, crs_wgs84, QgsProject.instance())
    ponto_wgs84 = trans1.transform(ponto)
    
    print(f"\n✅ Conversão SIRGAS 2000 → WGS84:")
    print(f"   Lon: {ponto_wgs84.x():.6f}°, Lat: {ponto_wgs84.y():.6f}°")
    
    # Conversão 2: WGS84 -> UTM
    trans2 = QgsCoordinateTransform(crs_wgs84, crs_utm, QgsProject.instance())
    ponto_utm = trans2.transform(ponto_wgs84)
    
    print(f"\n✅ Conversão WGS84 → UTM (Zona {zona}):")
    print(f"   X (Este): {ponto_utm.x():.2f} m")
    print(f"   Y (Norte): {ponto_utm.y():.2f} m")
    
    # Formato final
    coord_final = f"{int(round(ponto_utm.x()))} {int(round(ponto_utm.y()))} {zona}"
    print(f"\n📝 Formato Final:")
    print(f"   '{coord_final}'")
    
    print("\n" + "="*70)
    
    # Verificar se está em metros (UTM) ou graus
    if abs(ponto_utm.x()) > 1000:
        print("✅ SUCESSO: Coordenadas estão em METROS (UTM)!")
    else:
        print("❌ ERRO: Coordenadas ainda estão em GRAUS!")
    
    print("="*70)


def main():
    QgsApplication.setPrefixPath("C:/Program Files/QGIS*", True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    
    try:
        teste_conversao()
        return 0
    finally:
        qgs.exitQgis()


if __name__ == "__main__":
    sys.exit(main())
