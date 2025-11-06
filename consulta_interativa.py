#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Consulta de Coordenadas - Modo Interativo
Versão simplificada para executável standalone.

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
    QgsProject,
    QgsVectorLayer,
    QgsPointXY,
    QgsGeometry,
    QgsCoordinateReferenceSystem,
    QgsFeature
)


# ============================================
# CONFIGURAÇÕES GLOBAIS
# ============================================

# Detectar diretório base (para PyInstaller)
if getattr(sys, 'frozen', False):
    # Executando como executável
    BASE_DIR = Path(sys.executable).parent
else:
    # Executando como script
    BASE_DIR = Path(__file__).parent

SHAPES_DIR = BASE_DIR / "LARGURAS FXD"

# Mapeamento de zonas UTM para EPSG (SIRGAS 2000)
ZONA_EPSG = {
    23: 31983,  # UTM 23S
    24: 31984   # UTM 24S
}

# Prefixos de arquivos para pesquisa
PREFIXOS_SHAPEFILES = ['shape']
PREFIXOS_FXD = ['FXD']
PREFIXOS_MUNICIPIOS = ['municipios']


def limpar_tela():
    """Limpa a tela do console."""
    os.system('cls' if os.name == 'nt' else 'clear')


def exibir_banner():
    """Exibe o banner do sistema."""
    print("=" * 76)
    print("  CONSULTA DE COORDENADAS - SISTEMA RODOVIÁRIO")
    print("=" * 76)
    print()


def solicitar_coordenadas():
    """
    Solicita as coordenadas ao usuário de forma interativa.
    
    Returns:
        tuple: (x, y, zona) ou None se cancelado
    """
    try:
        print("Digite as coordenadas UTM (ou 'sair' para encerrar):")
        print()
        
        # Solicitar X
        x_input = input("  Coordenada X (Este): ").strip()
        if x_input.lower() in ['sair', 'exit', 'quit', 'q']:
            return None
        x = float(x_input)
        
        # Solicitar Y
        y_input = input("  Coordenada Y (Norte): ").strip()
        if y_input.lower() in ['sair', 'exit', 'quit', 'q']:
            return None
        y = float(y_input)
        
        # Solicitar Zona
        zona_input = input("  Zona UTM (23 ou 24): ").strip()
        if zona_input.lower() in ['sair', 'exit', 'quit', 'q']:
            return None
        zona = int(zona_input)
        
        return (x, y, zona)
    
    except ValueError:
        print("\n❌ ERRO: Valores inválidos. Digite apenas números.")
        return False
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário.")
        return None


def validar_coordenadas(x, y, zona):
    """Valida se as coordenadas UTM estão dentro dos limites esperados."""
    if zona not in ZONA_EPSG:
        print(f"❌ ERRO: Zona {zona} inválida. Use 23 ou 24.")
        return False
    
    if zona == 23:
        if not (160000 <= x <= 850000):
            print(f"❌ ERRO: Coordenada X {x} fora do range esperado para zona 23 (160000-850000)")
            return False
    elif zona == 24:
        if not (200000 <= x <= 850000):
            print(f"❌ ERRO: Coordenada X {x} fora do range esperado para zona 24 (200000-850000)")
            return False
    
    if not (8000000 <= y <= 9200000):
        print(f"❌ ERRO: Coordenada Y {y} fora do range esperado (8000000-9200000)")
        return False
    
    return True


def encontrar_shapefiles():
    """Encontra todos os shapefiles válidos no diretório."""
    shapefiles = []
    
    if not SHAPES_DIR.exists():
        print(f"❌ ERRO: Diretório {SHAPES_DIR} não encontrado!")
        return []
    
    for shp_file in SHAPES_DIR.glob("*.shp"):
        shapefiles.append(shp_file)
    
    return shapefiles


def carregar_camada(shapefile_path, nome_camada):
    """Carrega um shapefile como camada QGIS."""
    camada = QgsVectorLayer(str(shapefile_path), nome_camada, "ogr")
    
    if not camada.isValid():
        return None
    
    return camada


def consultar_coordenadas(x, y, zona):
    """
    Realiza a consulta das coordenadas nos shapefiles.
    Implementação completa do algoritmo de cálculo de KM.
    """
    from typing import Dict, Any, List, Optional, Tuple
    import re
    
    # Funções auxiliares (extraídas do consulta_standalone.py)
    def extrair_conexoes_trecho(nome_trecho: str) -> Dict[str, List[str]]:
        """Extrai as conexões de um trecho a partir do nome."""
        conexoes = {
            'origem': [],
            'destino': []
        }
        
        padrao_entr = r'ENTR\s+([A-Z]{2}\s*-?\s*\d{3})'
        padrao_trecho_origem = r'^ENTR\s+([A-Z]{2}\s*-?\s*\d{3})'
        padrao_trecho_destino = r'-\s*ENTR\s+([A-Z]{2}\s*-?\s*\d{3})'
        
        matches_origem = re.findall(padrao_trecho_origem, nome_trecho.upper())
        for match in matches_origem:
            rodovia = match.replace(' ', '').replace('-', ' - ')
            conexoes['origem'].append(rodovia)
        
        matches_destino = re.findall(padrao_trecho_destino, nome_trecho.upper())
        for match in matches_destino:
            rodovia = match.replace(' ', '').replace('-', ' - ')
            conexoes['destino'].append(rodovia)
        
        if not conexoes['destino']:
            todas_entradas = re.findall(padrao_entr, nome_trecho.upper())
            if todas_entradas:
                if len(todas_entradas) > len(conexoes['origem']):
                    conexoes['destino'] = [r.replace(' ', '').replace('-', ' - ') 
                                          for r in todas_entradas[len(conexoes['origem']):]]
        
        return conexoes
    
    
    def verificar_continuidade_trechos(trecho1_nome: str, trecho2_nome: str) -> bool:
        """Verifica se dois trechos são contínuos."""
        conexoes1 = extrair_conexoes_trecho(trecho1_nome)
        conexoes2 = extrair_conexoes_trecho(trecho2_nome)
        
        for destino1 in conexoes1['destino']:
            for origem2 in conexoes2['origem']:
                if destino1 == origem2:
                    return True
        
        return False
    
    
    def calcular_km_no_eixo(ponto: QgsPointXY, geometria: QgsGeometry, 
                           km_inicial: float, km_final: float,
                           codigo_sre_atual: str, nome_trecho: str,
                           todas_features: List) -> float:
        """Calcula o KM no eixo com detecção inteligente de orientação."""
        
        if geometria.isMultipart():
            linha = geometria.asMultiPolyline()[0]
        else:
            linha = geometria.asPolyline()
        
        ponto_mais_proximo = geometria.nearestPoint(QgsGeometry.fromPointXY(ponto))
        distancia_total = geometria.length()
        distancia_percorrida = 0.0
        
        ponto_proximo_coords = ponto_mais_proximo.asPoint()
        
        for i in range(len(linha) - 1):
            p1 = linha[i]
            p2 = linha[i + 1]
            
            segmento = QgsGeometry.fromPolylineXY([p1, p2])
            ponto_proximo_segmento = segmento.nearestPoint(QgsGeometry.fromPointXY(ponto_proximo_coords))
            
            if ponto_proximo_segmento.asPoint().distance(ponto_proximo_coords) < 0.01:
                distancia_p1_proximo = QgsGeometry.fromPointXY(p1).distance(ponto_proximo_segmento)
                distancia_percorrida += distancia_p1_proximo
                break
            else:
                distancia_percorrida += segmento.length()
        
        percentual = (distancia_percorrida / distancia_total) * 100 if distancia_total > 0 else 0
        
        comprimento_trecho = km_final - km_inicial
        km_opcao1 = km_inicial + (percentual / 100) * comprimento_trecho
        km_opcao2 = km_final - (percentual / 100) * comprimento_trecho
        
        # Análise de continuidade
        orientacao_validada = None
        continuidade_detectada = False
        
        if km_inicial < km_final:
            rodovia_codigo = codigo_sre_atual[:6]
            trechos_rodovia = []
            
            for feat in todas_features:
                cod_sre = feat.attribute('CODIGO_SRE')
                if cod_sre and cod_sre.startswith(rodovia_codigo):
                    trechos_rodovia.append({
                        'cod_sre': cod_sre,
                        'km_ini': feat.attribute('KM_INICIAL'),
                        'km_fim': feat.attribute('KM_FINAL'),
                        'trecho': feat.attribute('TRECHO')
                    })
            
            trechos_rodovia.sort(key=lambda x: x['cod_sre'])
            
            idx_atual = next((i for i, t in enumerate(trechos_rodovia) 
                            if t['cod_sre'] == codigo_sre_atual), -1)
            
            if idx_atual > 0:
                trecho_anterior = trechos_rodovia[idx_atual - 1]
                dif_km = abs(km_inicial - trecho_anterior['km_fim'])
                
                if dif_km < 0.5:
                    continuidade_detectada = True
            
            if idx_atual < len(trechos_rodovia) - 1:
                trecho_posterior = trechos_rodovia[idx_atual + 1]
                dif_km = abs(km_final - trecho_posterior['km_ini'])
                
                if dif_km < 0.5:
                    continuidade_detectada = True
            
            if continuidade_detectada and idx_atual > 0:
                trecho_anterior = trechos_rodovia[idx_atual - 1]
                
                dif_km_inicial = abs(km_inicial - trecho_anterior['km_fim'])
                dif_km_final = abs(km_final - trecho_anterior['km_fim'])
                
                if dif_km_inicial < dif_km_final:
                    if percentual < 50:
                        dist_opcao1_inicial = abs(km_opcao1 - km_inicial)
                        dist_opcao2_inicial = abs(km_opcao2 - km_inicial)
                        
                        if dist_opcao1_inicial < dist_opcao2_inicial:
                            orientacao_validada = 'normal'
                        else:
                            orientacao_validada = 'invertida'
                    else:
                        dist_opcao1_final = abs(km_opcao1 - km_final)
                        dist_opcao1_inicial = abs(km_opcao1 - km_inicial)
                        comprimento_trecho = km_final - km_inicial
                        
                        prox_final_percent = (dist_opcao1_final / comprimento_trecho) * 100
                        prox_inicial_percent = (dist_opcao1_inicial / comprimento_trecho) * 100
                        
                        if prox_final_percent < 10:
                            orientacao_validada = 'normal'
                        elif prox_inicial_percent < 10:
                            orientacao_validada = 'invertida'
                        elif dist_opcao1_inicial < dist_opcao1_final:
                            orientacao_validada = 'invertida'
                        else:
                            orientacao_validada = 'normal'
                else:
                    orientacao_validada = 'invertida'
            
            elif km_inicial < km_final and idx_atual == 0:
                if km_inicial < 1.0:
                    if percentual < 50:
                        dist_opcao1_inicial = abs(km_opcao1 - km_inicial)
                        dist_opcao2_inicial = abs(km_opcao2 - km_inicial)
                        
                        if dist_opcao1_inicial < dist_opcao2_inicial:
                            orientacao_validada = 'normal'
                        else:
                            orientacao_validada = 'invertida'
                    else:
                        dist_opcao1_final = abs(km_opcao1 - km_final)
                        dist_opcao2_final = abs(km_opcao2 - km_final)
                        
                        if dist_opcao1_final < dist_opcao2_final:
                            orientacao_validada = 'normal'
                        else:
                            orientacao_validada = 'invertida'
        
        if orientacao_validada == 'invertida':
            km_calculado = km_opcao2
        else:
            km_calculado = km_opcao1
        
        return round(km_calculado, 2)
    
    
    # Início da consulta
    epsg = ZONA_EPSG[zona]
    crs = QgsCoordinateReferenceSystem(f"EPSG:{epsg}")
    ponto_consulta = QgsPointXY(x, y)
    geom_ponto = QgsGeometry.fromPointXY(ponto_consulta)
    
    resultado = {
        'x': x,
        'y': y,
        'zona': zona,
        'dentro_fxd': False,
        'municipio': None,
        'info_eixo': None
    }
    
    shapefiles = encontrar_shapefiles()
    if not shapefiles:
        return None
    
    # 1. Verificar FXD
    for shp_path in shapefiles:
        nome = shp_path.stem.lower()
        if any(prefixo.lower() in nome for prefixo in PREFIXOS_FXD):
            if f"{zona}" not in nome:
                continue
            
            camada_fxd = carregar_camada(shp_path, "FXD")
            if not camada_fxd:
                continue
            
            for feature in camada_fxd.getFeatures():
                geom = feature.geometry()
                if geom.contains(geom_ponto):
                    resultado['dentro_fxd'] = True
                    print("\n✅ Ponto DENTRO da Faixa de Domínio")
                    break
            
            if resultado['dentro_fxd']:
                break
    
    # 2. Identificar município
    for shp_path in shapefiles:
        nome = shp_path.stem.lower()
        if any(prefixo.lower() in nome for prefixo in PREFIXOS_MUNICIPIOS):
            if f"{zona}" not in nome:
                continue
            
            camada_muni = carregar_camada(shp_path, "Municipios")
            if not camada_muni:
                continue
            
            for feature in camada_muni.getFeatures():
                geom = feature.geometry()
                if geom.contains(geom_ponto):
                    resultado['municipio'] = feature.attribute('NM_MUN')
                    break
            
            if resultado['municipio']:
                break
    
    # 3. Buscar eixo rodoviário
    for shp_path in shapefiles:
        nome = shp_path.stem.lower()
        if any(prefixo.lower() in nome for prefixo in PREFIXOS_SHAPEFILES):
            if f"{zona}" not in nome:
                continue
            
            camada_shape = carregar_camada(shp_path, "Eixos")
            if not camada_shape:
                continue
            
            todas_features = list(camada_shape.getFeatures())
            melhor_feature = None
            menor_distancia = float('inf')
            
            for feature in todas_features:
                geom = feature.geometry()
                distancia = geom.distance(geom_ponto)
                
                if distancia <= 200 and distancia < menor_distancia:
                    menor_distancia = distancia
                    melhor_feature = feature
            
            if melhor_feature:
                km_calculado = calcular_km_no_eixo(
                    ponto_consulta,
                    melhor_feature.geometry(),
                    melhor_feature.attribute('KM_INICIAL'),
                    melhor_feature.attribute('KM_FINAL'),
                    melhor_feature.attribute('CODIGO_SRE'),
                    melhor_feature.attribute('TRECHO'),
                    todas_features
                )
                
                resultado['info_eixo'] = {
                    'codigo_sre': melhor_feature.attribute('CODIGO_SRE'),
                    'rodovia': melhor_feature.attribute('RODOVIA'),
                    'trecho': melhor_feature.attribute('TRECHO'),
                    'jurisdicao': melhor_feature.attribute('JURISDICAO'),
                    'amparo_legal': melhor_feature.attribute('AMPARO_LEGA'),
                    'largura_fxd': melhor_feature.attribute('LARGURA_FX'),
                    'pavimentacao': melhor_feature.attribute('PAVIMENTAC'),
                    'km_calculado': km_calculado,
                    'distancia_eixo': round(menor_distancia, 2)
                }
                break
    
    return resultado


def exibir_resultado(resultado):
    """Exibe o resultado da consulta de forma formatada."""
    print("\n" + "=" * 76)
    
    if resultado['dentro_fxd']:
        print("⚠️  DENTRO DA FXD")
    else:
        print("✅ FORA DA FXD")
    
    print("=" * 76)
    print()
    
    if resultado['info_eixo']:
        info = resultado['info_eixo']
        rodovia_num = info['rodovia'].replace('BA', '').strip()
        
        print(f"CÓDIGO SRE:        {info['codigo_sre']}")
        print(f"RODOVIA:           BA - {rodovia_num}")
        print(f"TRECHO:            {info['trecho']}")
        print(f"MUNICÍPIO:         {resultado['municipio'].upper() if resultado['municipio'] else 'N/A'}")
        print(f"KM CALCULADO:      {info['km_calculado']:.2f} km")
        print(f"JURISDIÇÃO:        {info['jurisdicao']}")
        print(f"AMPARO LEGAL:      {info['amparo_legal']}")
        print(f"LARGURA FXD:       {info['largura_fxd']}")
        print(f"PAVIMENTAÇÃO:      {info['pavimentacao']}")
        print(f"DISTÂNCIA DO EIXO: {info['distancia_eixo']:.2f} m")
    else:
        print("❌ Nenhum eixo rodoviário encontrado próximo ao ponto.")
        if resultado['municipio']:
            print(f"MUNICÍPIO:         {resultado['municipio'].upper()}")
    
    print()


def main():
    """Função principal em modo interativo."""
    
    # Inicializar QGIS
    QgsApplication.setPrefixPath("", True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    
    try:
        while True:
            limpar_tela()
            exibir_banner()
            
            # Solicitar coordenadas
            coords = solicitar_coordenadas()
            
            if coords is None:
                # Usuário cancelou
                print("\n👋 Encerrando sistema...")
                break
            
            if coords is False:
                # Erro de validação
                input("\nPressione ENTER para continuar...")
                continue
            
            x, y, zona = coords
            
            # Validar coordenadas
            print()
            if not validar_coordenadas(x, y, zona):
                input("\nPressione ENTER para continuar...")
                continue
            
            # Executar consulta
            print("\n🔍 Consultando...")
            resultado = consultar_coordenadas(x, y, zona)
            
            if resultado:
                exibir_resultado(resultado)
            else:
                print("\n❌ Consulta sem resultados.")
            
            # Perguntar se deseja fazer outra consulta
            print()
            continuar = input("Deseja fazer outra consulta? (S/N): ").strip().upper()
            if continuar not in ['S', 'SIM', 'Y', 'YES']:
                print("\n👋 Encerrando sistema...")
                break
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Sistema interrompido pelo usuário.")
    
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Finalizar QGIS
        qgs.exitQgis()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
