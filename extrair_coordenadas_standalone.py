#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Standalone para extrair coordenadas de início e fim de geometrias lineares
e adicionar à tabela de atributos do shapefile.

Uso: python extrair_coordenadas_standalone.py <caminho_shapefile>

Autor: Sistema de Gestão Rodoviária
Data: 2025
"""

import sys
import os
from pathlib import Path

# Configuração PyQGIS
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from qgis.core import (
    QgsApplication,
    QgsVectorLayer,
    QgsField,
    QgsVectorFileWriter,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
    QgsPointXY
)
from qgis.PyQt.QtCore import QVariant


def calcular_zona_utm(longitude):
    """
    Calcula a zona UTM com base na longitude.
    Para o Brasil (Hemisfério Sul), zonas 18-25.
    
    Args:
        longitude: Longitude em graus decimais
    
    Returns:
        Número da zona UTM (18-25 para Brasil)
    """
    # Fórmula padrão: zona = int((longitude + 180) / 6) + 1
    zona = int((longitude + 180) / 6) + 1
    
    # Para o Brasil (especificamente Bahia), espera-se zonas 23 e 24
    # Zona 23: longitude aproximada -48° a -42°
    # Zona 24: longitude aproximada -42° a -36°
    
    return zona


def extrair_coordenadas_inicio_fim(caminho_shapefile):
    """
    Extrai coordenadas de início e fim de cada feição linear e adiciona
    os campos 'c_inicial' e 'c_final' à tabela de atributos.
    
    Args:
        caminho_shapefile: Caminho completo para o shapefile
    
    Returns:
        True se bem-sucedido, False caso contrário
    """
    try:
        print("="*70)
        print("🔧 EXTRATOR DE COORDENADAS - INÍCIO/FIM DE RODOVIAS")
        print("="*70)
        print(f"\n📁 Shapefile: {caminho_shapefile}")
        
        # Verificar se o arquivo existe
        if not Path(caminho_shapefile).exists():
            print(f"❌ ERRO: Arquivo não encontrado!")
            return False
        
        # Carregar o shapefile
        layer = QgsVectorLayer(caminho_shapefile, "rodovias", "ogr")
        
        if not layer.isValid():
            print("❌ ERRO: Não foi possível carregar o shapefile!")
            return False
        
        # Verificar se é um layer de linhas
        if layer.geometryType() != 1:  # 1 = LineString
            print("❌ ERRO: O shapefile deve conter geometrias lineares (linhas)!")
            print(f"   Tipo detectado: {layer.geometryType()}")
            return False
        
        print(f"✅ Shapefile carregado com sucesso!")
        print(f"   Total de feições: {layer.featureCount()}")
        print(f"   Sistema de coordenadas: {layer.crs().authid()}")
        
        # Verificar se os campos já existem
        field_names = [field.name() for field in layer.fields()]
        campos_existem = (
            'c_inicial' in field_names and 
            'c_final' in field_names
        )
        
        if not campos_existem:
            print("\n➕ Campos não existem, serão criados:")
            print("   - c_inicial: Coordenadas de início (X Y Zona)")
            print("   - c_final: Coordenadas de fim (X Y Zona)")
            print("   Formato: 412312 8123123 24")
        else:
            print("\n⚠️  AVISO: Campos já existem e serão sobrescritos!")
        
        # Iniciar edição
        if not layer.startEditing():
            print("❌ ERRO: Não foi possível iniciar edição do layer!")
            return False
        
        # Adicionar campos se não existirem
        campos_adicionados = []
        
        if 'c_inicial' not in field_names:
            if layer.addAttribute(QgsField('c_inicial', QVariant.String, len=30)):
                campos_adicionados.append('c_inicial')
            else:
                print("❌ ERRO: Não foi possível adicionar campo 'c_inicial'!")
        
        if 'c_final' not in field_names:
            if layer.addAttribute(QgsField('c_final', QVariant.String, len=30)):
                campos_adicionados.append('c_final')
            else:
                print("❌ ERRO: Não foi possível adicionar campo 'c_final'!")
        
        if campos_adicionados:
            layer.updateFields()
            print(f"   ✅ Campos adicionados: {', '.join(campos_adicionados)}")
        else:
            print("   ℹ️  Todos os campos já existem, apenas atualizando valores...")
        
        # Processar feições
        print("\n🔄 Processando feições...")
        
        features_processadas = 0
        features_erro = 0
        
        # Obter índices dos campos
        layer.updateFields()
        idx_c_inicial = layer.fields().indexOf('c_inicial')
        idx_c_final = layer.fields().indexOf('c_final')
        
        if idx_c_inicial == -1 or idx_c_final == -1:
            print("❌ ERRO: Não foi possível encontrar os campos criados!")
            layer.rollBack()
            return False
        
        for feature in layer.getFeatures():
            try:
                geom = feature.geometry()
                
                if geom.isEmpty():
                    print(f"   ⚠️  Feature ID {feature.id()}: geometria vazia - pulando")
                    features_erro += 1
                    continue
                
                # Extrair pontos de início e fim
                if geom.isMultipart():
                    lines = geom.asMultiPolyline()
                    if not lines or len(lines) == 0:
                        features_erro += 1
                        continue
                    # Pega a primeira linha da multilinha
                    first_line = lines[0]
                    # Pega a última linha da multilinha
                    last_line = lines[-1]
                    ponto_inicial = first_line[0]
                    ponto_final = last_line[-1]
                else:
                    line = geom.asPolyline()
                    if not line or len(line) == 0:
                        features_erro += 1
                        continue
                    ponto_inicial = line[0]
                    ponto_final = line[-1]
                
                # Obter sistema de coordenadas atual
                crs_atual = layer.crs()
                
                # Primeiro, sempre converter para WGS84 (lat/lon) para calcular a zona correta
                crs_latlon = QgsCoordinateReferenceSystem("EPSG:4326")  # WGS84
                
                transformador_para_latlon = QgsCoordinateTransform(
                    crs_atual, 
                    crs_latlon, 
                    QgsProject.instance()
                )
                
                # Converter pontos para lat/lon
                ponto_inicial_latlon = transformador_para_latlon.transform(ponto_inicial)
                ponto_final_latlon = transformador_para_latlon.transform(ponto_final)
                
                # Calcular zona UTM baseado na longitude
                zona_inicial = calcular_zona_utm(ponto_inicial_latlon.x())
                zona_final = calcular_zona_utm(ponto_final_latlon.x())
                
                # DEBUG: Primeira feição - mostrar detalhes da conversão
                if features_processadas == 0:
                    print(f"\n   🔍 DEBUG - Primeira feição:")
                    print(f"      CRS Original: {crs_atual.authid()} - {crs_atual.description()}")
                    print(f"      Ponto Inicial Original: X={ponto_inicial.x():.6f}, Y={ponto_inicial.y():.6f}")
                    print(f"      Ponto Inicial Lat/Lon: Lon={ponto_inicial_latlon.x():.6f}, Lat={ponto_inicial_latlon.y():.6f}")
                    print(f"      Zona UTM Calculada: {zona_inicial}")
                
                # IMPORTANTE: Agora converter de lat/lon (WGS84) para SIRGAS 2000 UTM
                # SIRGAS 2000 / UTM zone ##S: EPSG = 31960 + zona
                # Zona 23S = EPSG:31983 (31960 + 23)
                # Zona 24S = EPSG:31984 (31960 + 24)
                epsg_inicial = 31960 + zona_inicial
                epsg_final = 31960 + zona_final
                
                crs_utm_inicial = QgsCoordinateReferenceSystem(f"EPSG:{epsg_inicial}")
                crs_utm_final = QgsCoordinateReferenceSystem(f"EPSG:{epsg_final}")
                
                # Transformar de lat/lon (WGS84) para UTM (SIRGAS 2000)
                transformador_inicial = QgsCoordinateTransform(
                    crs_latlon,  # De WGS84 lat/lon
                    crs_utm_inicial,  # Para SIRGAS UTM
                    QgsProject.instance()
                )
                
                transformador_final = QgsCoordinateTransform(
                    crs_latlon,  # De WGS84 lat/lon
                    crs_utm_final,  # Para SIRGAS UTM
                    QgsProject.instance()
                )
                
                # Aplicar transformação nos pontos lat/lon
                ponto_inicial_utm = transformador_inicial.transform(ponto_inicial_latlon)
                ponto_final_utm = transformador_final.transform(ponto_final_latlon)
                
                # DEBUG: Primeira feição - mostrar coordenadas UTM
                if features_processadas == 0:
                    print(f"      CRS UTM Destino: {crs_utm_inicial.authid()} - {crs_utm_inicial.description()}")
                    print(f"      Ponto Inicial UTM: X={ponto_inicial_utm.x():.2f}, Y={ponto_inicial_utm.y():.2f}")
                    print(f"      ✅ Conversão realizada!\n")
                
                # Formatar coordenadas no formato: X Y Zona (sem vírgulas, valores inteiros)
                coord_inicial = f"{int(round(ponto_inicial_utm.x()))} {int(round(ponto_inicial_utm.y()))} {zona_inicial}"
                coord_final = f"{int(round(ponto_final_utm.x()))} {int(round(ponto_final_utm.y()))} {zona_final}"
                
                # DEBUG: mostrar coordenadas calculadas para a primeira feição
                if features_processadas == 0:
                    print(f"\n   🎯 VALORES A SEREM SALVOS NA PRIMEIRA FEIÇÃO:")
                    print(f"      c_inicial (índice {idx_c_inicial}): '{coord_inicial}'")
                    print(f"      c_final   (índice {idx_c_final}): '{coord_final}'")
                
                # Atualizar atributos
                if not layer.changeAttributeValue(feature.id(), idx_c_inicial, coord_inicial):
                    print(f"   ⚠️  Erro ao atualizar c_inicial para feature {feature.id()}")
                
                if not layer.changeAttributeValue(feature.id(), idx_c_final, coord_final):
                    print(f"   ⚠️  Erro ao atualizar c_final para feature {feature.id()}")
                
                features_processadas += 1
                
                # Mostrar progresso a cada 50 feições
                if features_processadas % 50 == 0:
                    print(f"   Processadas: {features_processadas} feições...")
            
            except Exception as e:
                print(f"   ❌ Erro ao processar feature ID {feature.id()}: {e}")
                features_erro += 1
                continue
        
        # Confirmar alterações
        print("\n💾 Salvando alterações...")
        if layer.commitChanges():
            print("✅ Alterações salvas com sucesso!")
        else:
            print("❌ ERRO ao salvar alterações:")
            for error in layer.commitErrors():
                print(f"   - {error}")
            layer.rollBack()
            return False
        
        # Resumo
        print("\n" + "="*70)
        print("📊 RESUMO DA OPERAÇÃO")
        print("="*70)
        print(f"✅ Feições processadas com sucesso: {features_processadas}")
        if features_erro > 0:
            print(f"⚠️  Feições com erro: {features_erro}")
        print(f"📁 Arquivo atualizado: {caminho_shapefile}")
        print("="*70)
        
        return True
    
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Função principal - execução CLI."""
    
    print("🔧 Inicializando PyQGIS...")
    
    # Inicializar QGIS
    QgsApplication.setPrefixPath("C:/Program Files/QGIS*", True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    
    try:
        # Verificar argumentos
        if len(sys.argv) < 2:
            print("\n❌ ERRO: Caminho do shapefile não fornecido!")
            print("\nUso:")
            print("   python extrair_coordenadas_standalone.py <caminho_shapefile>")
            print("\nExemplo:")
            print('   python extrair_coordenadas_standalone.py "C:\\shapes\\rodovias.shp"')
            return 1
        
        caminho_shapefile = sys.argv[1]
        
        # Executar extração
        sucesso = extrair_coordenadas_inicio_fim(caminho_shapefile)
        
        if sucesso:
            print("\n✅ Operação concluída com sucesso!")
            return 0
        else:
            print("\n❌ Operação falhou. Verifique os erros acima.")
            return 1
    
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        return 2
    
    finally:
        # Finalizar QGIS
        qgs.exitQgis()


if __name__ == "__main__":
    sys.exit(main())
