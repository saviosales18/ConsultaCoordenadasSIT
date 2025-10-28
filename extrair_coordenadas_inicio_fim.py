#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para extrair coordenadas de início e fim de geometrias lineares
e adicionar à tabela de atributos do shapefile.

Este script deve ser executado no Console Python do QGIS.

Autor: Sistema de Gestão Rodoviária
Data: 2025
"""

from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsField,
    QgsFeature,
    edit
)
from qgis.PyQt.QtCore import QVariant
from pathlib import Path


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
        layer = QgsVectorLayer(caminho_shapefile, "temp_layer", "ogr")
        
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
        campos_existem = 'c_inicial' in field_names and 'c_final' in field_names
        
        if campos_existem:
            print("\n⚠️  AVISO: Campos 'c_inicial' e 'c_final' já existem!")
            resposta = input("   Deseja sobrescrever os valores? (s/n): ").lower()
            if resposta != 's':
                print("❌ Operação cancelada pelo usuário.")
                return False
        else:
            print("\n➕ Adicionando campos 'c_inicial' e 'c_final'...")
            
            # Iniciar edição
            layer.startEditing()
            
            # Adicionar campos
            layer.addAttribute(QgsField('c_inicial', QVariant.String, len=50))
            layer.addAttribute(QgsField('c_final', QVariant.String, len=50))
            
            # Confirmar adição
            layer.commitChanges()
            print("   ✅ Campos adicionados com sucesso!")
        
        # Processar feições
        print("\n🔄 Processando feições...")
        layer.startEditing()
        
        features_processadas = 0
        features_erro = 0
        
        # Obter índices dos campos
        idx_c_inicial = layer.fields().indexOf('c_inicial')
        idx_c_final = layer.fields().indexOf('c_final')
        
        for feature in layer.getFeatures():
            try:
                geom = feature.geometry()
                
                if geom.isEmpty():
                    print(f"   ⚠️  Feature ID {feature.id()}: geometria vazia - pulando")
                    features_erro += 1
                    continue
                
                # Extrair pontos de início e fim
                # Para MultiLineString, pega a primeira linha
                if geom.isMultipart():
                    lines = geom.asMultiPolyline()
                    if not lines or len(lines) == 0:
                        features_erro += 1
                        continue
                    first_line = lines[0]
                    ponto_inicial = first_line[0]
                    ponto_final = first_line[-1]
                else:
                    line = geom.asPolyline()
                    if not line or len(line) == 0:
                        features_erro += 1
                        continue
                    ponto_inicial = line[0]
                    ponto_final = line[-1]
                
                # Formatar coordenadas (X, Y) com 2 casas decimais
                coord_inicial = f"{ponto_inicial.x():.2f}, {ponto_inicial.y():.2f}"
                coord_final = f"{ponto_final.x():.2f}, {ponto_final.y():.2f}"
                
                # Atualizar atributos
                layer.changeAttributeValue(feature.id(), idx_c_inicial, coord_inicial)
                layer.changeAttributeValue(feature.id(), idx_c_final, coord_final)
                
                features_processadas += 1
                
                # Mostrar progresso a cada 100 feições
                if features_processadas % 100 == 0:
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
            return False
        
        # Resumo
        print("\n" + "="*70)
        print("📊 RESUMO DA OPERAÇÃO")
        print("="*70)
        print(f"✅ Feições processadas: {features_processadas}")
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


def processar_shapefile_interativo():
    """
    Versão interativa para uso no Console Python do QGIS.
    """
    print("\n🎯 MODO INTERATIVO - EXTRATOR DE COORDENADAS")
    print("="*70)
    
    # Solicitar caminho do shapefile
    print("\n📝 Digite o caminho completo do shapefile:")
    print("   Exemplo: C:/Users/savio/OneDrive/Documentos/repositories/ConsultaCoordenadasSIT/LARGURAS FXD/shapesFederais_07-2025.shp")
    
    caminho = input("\nCaminho: ").strip()
    
    # Remover aspas se houver
    caminho = caminho.strip('"').strip("'")
    
    if not caminho:
        print("❌ Nenhum caminho fornecido!")
        return
    
    # Processar
    sucesso = extrair_coordenadas_inicio_fim(caminho)
    
    if sucesso:
        print("\n✅ Operação concluída com sucesso!")
        print("💡 Você pode agora abrir o shapefile no QGIS e verificar os novos campos.")
    else:
        print("\n❌ Operação falhou. Verifique os erros acima.")


# ============================================
# EXECUÇÃO DIRETA (Console Python do QGIS)
# ============================================

if __name__ == '__main__':
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║  EXTRATOR DE COORDENADAS - INÍCIO/FIM DE RODOVIAS                ║
║                                                                   ║
║  Este script adiciona os campos 'c_inicial' e 'c_final' à        ║
║  tabela de atributos de um shapefile de rodovias (linhas).       ║
║                                                                   ║
║  COMO USAR:                                                       ║
║  1. Abra o QGIS                                                   ║
║  2. Vá em: Plugins > Console Python                              ║
║  3. Clique em "Mostrar Editor" (ícone de página)                 ║
║  4. Clique em "Abrir Script" e selecione este arquivo            ║
║  5. Clique em "Executar Script" (ícone de play verde)            ║
║  6. Digite o caminho do shapefile quando solicitado              ║
║                                                                   ║
║  OU use diretamente no console:                                  ║
║  >>> extrair_coordenadas_inicio_fim('caminho/do/seu/shape.shp')  ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    # Modo interativo
    processar_shapefile_interativo()


# ============================================
# EXEMPLOS DE USO NO CONSOLE DO QGIS
# ============================================

"""
EXEMPLO 1 - Processar shapefile específico:
--------------------------------------------
caminho = r"C:\Users\savio\OneDrive\Documentos\repositories\ConsultaCoordenadasSIT\LARGURAS FXD\shapesFederais_07-2025.shp"
extrair_coordenadas_inicio_fim(caminho)


EXEMPLO 2 - Processar múltiplos shapefiles:
--------------------------------------------
from pathlib import Path

pasta = Path(r"C:\Users\savio\OneDrive\Documentos\repositories\ConsultaCoordenadasSIT\LARGURAS FXD")

for shapefile in pasta.glob("shape*.shp"):
    print(f"\n🔄 Processando: {shapefile.name}")
    extrair_coordenadas_inicio_fim(str(shapefile))


EXEMPLO 3 - Processar layer ativo no QGIS:
--------------------------------------------
layer = iface.activeLayer()
if layer:
    caminho = layer.source().split("|")[0]
    extrair_coordenadas_inicio_fim(caminho)
else:
    print("❌ Nenhum layer ativo!")
"""
