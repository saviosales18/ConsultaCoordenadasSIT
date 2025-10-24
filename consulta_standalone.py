#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Consulta de Coordenadas - PyQGIS Standalone
Consulta coordenadas UTM em shapefiles de rodovias e calcula KM exato.

Autor: Sistema de Gestão Rodoviária
Data: 2025
"""

import sys
import os
import argparse
from pathlib import Path
from typing import Tuple, Optional, Dict, Any, List

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

QGIS_PATH = r"C:\Program Files\QGIS 3.12"
SHAPES_DIR = Path(__file__).parent / "LARGURAS FXD"

# Mapeamento de zonas UTM para EPSG (SIRGAS 2000)
ZONA_EPSG = {
    23: 31983,  # UTM 23S
    24: 31984   # UTM 24S
}

# Prefixos de arquivos para pesquisa
PREFIXOS_SHAPEFILES = ['shape']  # Apenas eixos rodoviários (linhas)
PREFIXOS_FXD = ['FXD']  # Faixa de Domínio (polígonos)
PREFIXOS_MUNICIPIOS = ['municipios']  # Municípios


# ============================================
# FUNÇÕES AUXILIARES - VALIDAÇÃO
# ============================================

def validar_coordenadas(x: float, y: float, zona: int) -> bool:
    """
    Valida se as coordenadas UTM estão dentro dos limites esperados.
    
    Args:
        x: Coordenada X (Este)
        y: Coordenada Y (Norte)
        zona: Zona UTM (23 ou 24)
    
    Returns:
        True se válidas, False caso contrário
    """
    if zona not in ZONA_EPSG:
        print(f"❌ ERRO: Zona {zona} inválida. Use 23 ou 24.")
        return False
    
    # Validação de coordenadas UTM por zona (Bahia)
    if zona == 23:
        # Zona 23: Oeste da Bahia (valores X menores)
        if not (160000 <= x <= 850000):
            print(f"❌ ERRO: Coordenada X {x} fora do range esperado para zona 23 (160000-850000)")
            return False
    elif zona == 24:
        # Zona 24: Leste da Bahia (valores X maiores)
        if not (200000 <= x <= 850000):
            print(f"❌ ERRO: Coordenada X {x} fora do range esperado para zona 24 (200000-850000)")
            return False
    
    # Coordenada Y válida para toda Bahia
    if not (8000000 <= y <= 9200000):
        print(f"❌ ERRO: Coordenada Y {y} fora do range esperado (8000000-9200000)")
        return False
    
    return True


def encontrar_shapefiles() -> list:
    """
    Encontra todos os shapefiles válidos no diretório.
    
    Returns:
        Lista de caminhos para os shapefiles encontrados
    """
    shapefiles = []
    
    if not SHAPES_DIR.exists():
        print(f"❌ ERRO: Diretório {SHAPES_DIR} não encontrado!")
        return []
    
    for prefixo in PREFIXOS_SHAPEFILES:
        for shape in SHAPES_DIR.glob(f"{prefixo}*.shp"):
            shapefiles.append(str(shape))
    
    if not shapefiles:
        print(f"❌ AVISO: Nenhum shapefile encontrado em {SHAPES_DIR}")
    
    return shapefiles


def buscar_municipio_por_coordenadas(ponto: QgsPointXY, zona: int) -> Optional[str]:
    """
    Busca o município através de intersecção com shapefile de municípios.
    
    Args:
        ponto: Ponto de consulta
        zona: Zona UTM
    
    Returns:
        Nome do município ou None
    """
    try:
        # Procurar shapefile de municípios
        municipios_shapes = []
        for pattern in ['municipio*.shp', 'munic*.shp']:
            municipios_shapes.extend(SHAPES_DIR.glob(pattern))
        
        if not municipios_shapes:
            return None
        
        # Criar geometria do ponto
        ponto_geom = QgsGeometry.fromPointXY(ponto)
        
        # Tentar cada shapefile de municípios
        for shape_path in municipios_shapes:
            layer = QgsVectorLayer(str(shape_path), "municipios", "ogr")
            
            if not layer.isValid():
                continue
            
            # Buscar feição que contém o ponto
            for feature in layer.getFeatures():
                geom = feature.geometry()
                
                if geom.contains(ponto_geom):
                    # Buscar campo com nome do município
                    fields = [f.name() for f in layer.fields()]
                    attrs = feature.attributes()
                    
                    for i, field in enumerate(fields):
                        field_upper = field.upper()
                        if any(x in field_upper for x in ['MUNICIPIO', 'MUNIC', 'NOME', 'NM_MUN']):
                            return attrs[i]
                    
                    # Se não encontrou campo específico, retorna primeiro campo de texto
                    return attrs[0] if attrs else None
        
        return None
    
    except Exception as e:
        print(f"⚠️  Aviso ao buscar município: {e}")
        return None


# ============================================
# FUNÇÕES AUXILIARES - CÁLCULO DE KM
# ============================================

def extrair_conexoes_trecho(trecho: str) -> Dict[str, List[str]]:
    """
    Extrai pontos de conexão (entroncamentos) de um trecho.
    
    Args:
        trecho: String do trecho (ex: "ENTR BA 526(P/CIA) - ENTR BR 324(km 615,9)")
    
    Returns:
        Dict com 'inicio' e 'fim', cada um contendo lista de rodovias conectadas
    """
    import re
    
    conexoes = {'inicio': [], 'fim': []}
    
    if not trecho or ' - ' not in trecho:
        return conexoes
    
    partes = trecho.split(' - ')
    if len(partes) != 2:
        return conexoes
    
    inicio, fim = partes[0].strip(), partes[1].strip()
    
    # Padrões para extrair códigos de rodovias
    # Ex: "ENTR BA 526", "ENTR BR 324", "BA-001", "BR-101"
    padroes = [
        r'(?:ENTR\s+)?([A-Z]{2}[\s-]?\d{3})',  # BA 526, BR 324, BA-001
        r'(?:ACESSO\s+)?([A-Z]{2}[\s-]?\d{3})',  # ACESSO BA 099
    ]
    
    for texto, lista in [(inicio, conexoes['inicio']), (fim, conexoes['fim'])]:
        for padrao in padroes:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            for match in matches:
                # Normaliza: remove espaços e hífens
                rodovia = match.replace(' ', '').replace('-', '')
                if rodovia not in lista:
                    lista.append(rodovia)
    
    return conexoes


def verificar_continuidade_trechos(trecho_atual: str, trecho_comparacao: str, posicao: str) -> bool:
    """
    Verifica se dois trechos são contínuos (um termina onde o outro começa).
    
    Args:
        trecho_atual: Trecho atual sendo analisado
        trecho_comparacao: Trecho anterior ou posterior
        posicao: 'anterior' ou 'posterior'
    
    Returns:
        True se os trechos são contínuos
    """
    if not trecho_atual or not trecho_comparacao:
        return False
    
    conexoes_atual = extrair_conexoes_trecho(trecho_atual)
    conexoes_comp = extrair_conexoes_trecho(trecho_comparacao)
    
    if posicao == 'anterior':
        # Trecho anterior termina onde o atual começa
        # Fim do anterior deve corresponder ao início do atual
        return (
            any(rod in conexoes_atual['inicio'] for rod in conexoes_comp['fim']) or
            trecho_comparacao.split(' - ')[-1].strip() in trecho_atual
        )
    else:  # posterior
        # Trecho atual termina onde o posterior começa
        # Fim do atual deve corresponder ao início do posterior
        return (
            any(rod in conexoes_comp['inicio'] for rod in conexoes_atual['fim']) or
            trecho_atual.split(' - ')[-1].strip() in trecho_comparacao
        )


def calcular_km_no_eixo(geometria: QgsGeometry, ponto: QgsPointXY, 
                         km_inicial: float, km_final: float,
                         atributos: Dict[str, Any] = None,
                         todas_features: List[Tuple] = None) -> Optional[float]:
    """
    Calcula o KM no eixo rodoviário baseado na posição do ponto.
    Considera continuidade entre trechos para validar orientação da geometria.
    
    Args:
        geometria: Geometria do eixo rodoviário
        ponto: Ponto a ser projetado
        km_inicial: KM inicial do trecho
        km_final: KM final do trecho
        atributos: Atributos da feature atual (incluindo TRECHO)
        todas_features: Lista de todas as features para análise de continuidade
    
    Returns:
        KM calculado ou None se erro
    """
    try:
        # Projeta o ponto na linha
        ponto_projetado = geometria.nearestPoint(QgsGeometry.fromPointXY(ponto))
        if ponto_projetado.isEmpty():
            return None
        
        # Calcula distância ao longo da linha
        distancia_ao_longo = geometria.lineLocatePoint(ponto_projetado)
        comprimento_total = geometria.length()
        
        if comprimento_total == 0:
            return None
        
        # Calcula percentual percorrido
        percentual = (distancia_ao_longo / comprimento_total) * 100
        
        # Calcula ambas as opções
        proporcao = distancia_ao_longo / comprimento_total
        km_opcao1 = km_inicial + (proporcao * (km_final - km_inicial))  # Normal
        km_opcao2 = km_final - (proporcao * (km_final - km_inicial))    # Invertida
        
        # ====================================================================
        # VALIDAÇÃO POR CONTINUIDADE DE TRECHOS (NOVA LÓGICA)
        # ====================================================================
        orientacao_validada = None
        
        if atributos and todas_features:
            trecho_atual = atributos.get('TRECHO', '') or atributos.get('LOCAL_IN_', '') + ' - ' + atributos.get('LOCAL_FIM', '')
            rodovia_atual = atributos.get('RODOVIA', '')
            codigo_sre_atual = atributos.get('CÓDIGO SRE', atributos.get('COD_SRE', atributos.get('CODIGO_SRE', '')))
            
            if trecho_atual and rodovia_atual and codigo_sre_atual:
                # Busca trechos anterior e posterior na mesma rodovia
                trechos_rodovia = []
                
                for feat in todas_features:
                    feat_rodovia = feat[1].get('RODOVIA', '')
                    feat_cod_sre = feat[1].get('CÓDIGO SRE', feat[1].get('COD_SRE', feat[1].get('CODIGO_SRE', '')))
                    feat_km_ini = feat[1].get('KM_INICIAL')
                    feat_km_fim = feat[1].get('KM_FINAL')
                    feat_local_ini = feat[1].get('LOCAL_IN_', '')
                    feat_local_fim = feat[1].get('LOCAL_FIM', '')
                    
                    if feat_rodovia == rodovia_atual and feat_cod_sre and feat_km_ini is not None:
                        trechos_rodovia.append({
                            'cod_sre': feat_cod_sre,
                            'km_ini': float(feat_km_ini),
                            'km_fim': float(feat_km_fim) if feat_km_fim is not None else float(feat_km_ini),
                            'local_ini': feat_local_ini,
                            'local_fim': feat_local_fim
                        })
                
                # Ordena por código SRE (indica sequência lógica dos trechos)
                trechos_rodovia.sort(key=lambda x: x['cod_sre'])
                
                # Encontra índice do trecho atual
                idx_atual = None
                for i, t in enumerate(trechos_rodovia):
                    if t['cod_sre'] == codigo_sre_atual:
                        idx_atual = i
                        break
                
                if idx_atual is not None and len(trechos_rodovia) > 1:
                    continuidade_detectada = False
                    
                    # Verifica trecho anterior
                    if idx_atual > 0:
                        trecho_anterior = trechos_rodovia[idx_atual - 1]
                        
                        # O KM FINAL do anterior deve ser igual ao KM INICIAL do atual
                        dif_km = abs(trecho_anterior['km_fim'] - km_inicial)
                        
                        if dif_km < 0.5:  # Tolerância de 500m
                            continuidade_detectada = True
                            print(f"   ✅ Continuidade validada: {trecho_anterior['cod_sre']} (fim={trecho_anterior['km_fim']:.2f}) → {codigo_sre_atual} (ini={km_inicial:.2f})")
                    
                    # Verifica trecho posterior
                    if idx_atual < len(trechos_rodovia) - 1:
                        trecho_posterior = trechos_rodovia[idx_atual + 1]
                        
                        # O KM FINAL do atual deve ser igual ao KM INICIAL do posterior
                        dif_km = abs(km_final - trecho_posterior['km_ini'])
                        
                        if dif_km < 0.5:
                            continuidade_detectada = True
                            print(f"   ✅ Continuidade validada: {codigo_sre_atual} (fim={km_final:.2f}) → {trecho_posterior['cod_sre']} (ini={trecho_posterior['km_ini']:.2f})")
                    
                    # Se há continuidade validada, detectar orientação da geometria
                    if continuidade_detectada and idx_atual is not None:
                        # ESTRATÉGIA DEFINITIVA: Usar continuidade para determinar orientação
                        # Se temos trecho anterior: o fim do anterior deve conectar com o início do atual
                        # Isso nos diz QUAL extremo do trecho atual é o "início lógico"
                        
                        if km_inicial < km_final and idx_atual > 0:
                            # Temos trecho anterior - verificar qual extremo conecta
                            trecho_anterior = trechos_rodovia[idx_atual - 1]
                            km_fim_anterior = trecho_anterior['km_fim']
                            
                            # Qual extremo do trecho atual está mais próximo do fim do anterior?
                            dist_inicial_anterior = abs(km_inicial - km_fim_anterior)
                            dist_final_anterior = abs(km_final - km_fim_anterior)
                            
                            if dist_inicial_anterior < dist_final_anterior:
                                # KM_INICIAL conecta com o anterior = início lógico é KM_INICIAL
                                # Portanto: geometria deveria começar no percentual 0% e ir até 100%
                                # Se percentual BAIXO resulta em KM próximo de KM_INICIAL → NORMAL
                                # Se percentual ALTO resulta em KM próximo de KM_INICIAL → INVERTIDA
                                
                                # Testar: onde está o ponto na geometria?
                                if percentual < 50:  # Início da geometria
                                    # Início da geometria deve ter KM baixo (próximo de KM_INICIAL)
                                    dist_opcao1_inicial = abs(km_opcao1 - km_inicial)
                                    dist_opcao2_inicial = abs(km_opcao2 - km_inicial)
                                    
                                    if dist_opcao1_inicial < dist_opcao2_inicial:
                                        orientacao_validada = 'normal'
                                        print(f"   🎯 Geometria NORMAL: início geom + KM próximo de inicial")
                                    else:
                                        orientacao_validada = 'invertida'
                                        print(f"   🎯 Geometria INVERTIDA: início geom + KM longe de inicial")
                                else:  # Fim da geometria (percentual >= 50%)
                                    # Fim da geometria deve ter KM alto (próximo de KM_FINAL)
                                    # Testar se km_opcao1 (cálculo normal) está próximo do fim
                                    dist_opcao1_final = abs(km_opcao1 - km_final)
                                    dist_opcao1_inicial = abs(km_opcao1 - km_inicial)
                                    comprimento_trecho = km_final - km_inicial
                                    
                                    # Calcular proximidade RELATIVA (em % do comprimento do trecho)
                                    prox_final_percent = (dist_opcao1_final / comprimento_trecho) * 100
                                    prox_inicial_percent = (dist_opcao1_inicial / comprimento_trecho) * 100
                                    
                                    # Se está dentro de 10% do fim, considera próximo do fim
                                    if prox_final_percent < 10:
                                        # Muito próximo do fim = NORMAL
                                        orientacao_validada = 'normal'
                                        print(f"   🎯 Geometria NORMAL: fim geom + opcao1 {prox_final_percent:.1f}% do final")
                                    elif prox_inicial_percent < 10:
                                        # Muito próximo do início = INVERTIDA
                                        orientacao_validada = 'invertida'
                                        print(f"   🎯 Geometria INVERTIDA: fim geom + opcao1 {prox_inicial_percent:.1f}% do inicial")
                                    elif dist_opcao1_inicial < dist_opcao1_final:
                                        # Mais próximo do início = INVERTIDA
                                        orientacao_validada = 'invertida'
                                        print(f"   🎯 Geometria INVERTIDA: fim geom mas opcao1={km_opcao1:.2f} mais próximo de inicial")
                                    else:
                                        # Mais próximo do fim = NORMAL
                                        orientacao_validada = 'normal'
                                        print(f"   🎯 Geometria NORMAL: fim geom e opcao1={km_opcao1:.2f} mais próximo de final")
                            else:
                                # KM_FINAL conecta com o anterior = início lógico é KM_FINAL
                                # Geometria foi desenhada invertida em relação à quilometragem
                                orientacao_validada = 'invertida'
                                print(f"   🎯 Geometria INVERTIDA: KM_FINAL ({km_final:.2f}) conecta com anterior")
                        
                        elif km_inicial < km_final and idx_atual == 0:
                            # Primeiro trecho da rodovia - usar KM 0 como referência
                            # Se km_inicial ≈ 0, o início lógico é KM_INICIAL
                            if km_inicial < 1.0:  # Começa próximo do KM 0
                                # Percentual baixo deve resultar em KM baixo
                                if percentual < 50:
                                    dist_opcao1_inicial = abs(km_opcao1 - km_inicial)
                                    dist_opcao2_inicial = abs(km_opcao2 - km_inicial)
                                    orientacao_validada = 'normal' if dist_opcao1_inicial < dist_opcao2_inicial else 'invertida'
                                    print(f"   🎯 Primeiro trecho: geometria {'NORMAL' if orientacao_validada == 'normal' else 'INVERTIDA'}")
                                else:
                                    dist_opcao1_final = abs(km_opcao1 - km_final)
                                    dist_opcao2_final = abs(km_opcao2 - km_final)
                                    orientacao_validada = 'normal' if dist_opcao1_final < dist_opcao2_final else 'invertida'
                                    print(f"   🎯 Primeiro trecho: geometria {'NORMAL' if orientacao_validada == 'normal' else 'INVERTIDA'}")
                            else:
                                # Não começa no KM 0 - usar heurística
                                orientacao_validada = 'normal'
                                print(f"   🎯 Primeiro trecho sem KM 0: assumindo NORMAL")
                        
                        elif km_inicial < km_final:
                            # Sem trecho anterior válido - usar heurística
                            if percentual > 70:
                                dist_opcao1_final = abs(km_opcao1 - km_final)
                                dist_opcao2_final = abs(km_opcao2 - km_final)
                                orientacao_validada = 'normal' if dist_opcao1_final < dist_opcao2_final else 'invertida'
                            else:
                                dist_opcao1_inicial = abs(km_opcao1 - km_inicial)
                                dist_opcao2_inicial = abs(km_opcao2 - km_inicial)
                                orientacao_validada = 'normal' if dist_opcao1_inicial < dist_opcao2_inicial else 'invertida'
                            print(f"   🎯 Heurística: geometria {'NORMAL' if orientacao_validada == 'normal' else 'INVERTIDA'}")
                        else:
                            # KM decrescente
                            orientacao_validada = 'normal'
                            print(f"   🎯 KM DECRESCENTE ({km_inicial:.2f} → {km_final:.2f})")
        
        # ====================================================================
        # ESCOLHA DO KM BASEADO EM VALIDAÇÃO
        # ====================================================================
        
        if orientacao_validada == 'normal':
            # Validação confirmou: usar cálculo normal
            km_calculado = km_opcao1
            debug_msg = f"✅ Orientação NORMAL validada por continuidade (KM {km_inicial:.2f} → {km_final:.2f})"
        elif orientacao_validada == 'invertida':
            # Validação confirmou: usar cálculo invertido
            km_calculado = km_opcao2
            debug_msg = f"✅ Orientação INVERTIDA validada por continuidade (KM {km_inicial:.2f} → {km_final:.2f})"
        else:
            # SEM VALIDAÇÃO: usar heurística baseada em crescente/decrescente
            if km_inicial < km_final:
                # KM crescente: geometria deve seguir ordem normal
                km_calculado = km_opcao1
                debug_msg = f"✅ Geometria NORMAL (KM crescente: {km_inicial:.2f} → {km_final:.2f})"
            else:
                # KM decrescente: geometria deve seguir ordem invertida
                km_calculado = km_opcao2
                debug_msg = f"✅ Geometria INVERTIDA (KM decrescente: {km_inicial:.2f} → {km_final:.2f})"
        
        # Debug info
        print(f"\n🔍 DEBUG KM:")
        print(f"   Percentual: {percentual:.1f}%")
        print(f"   Opção 1 (normal): {km_opcao1:.3f} km")
        print(f"   Opção 2 (invertida): {km_opcao2:.3f} km")
        print(f"   {debug_msg}")
        
        return km_calculado
    
    except Exception as e:
        print(f"❌ Erro ao calcular KM: {e}")
        return None


def calcular_distancia_do_eixo(ponto: QgsPointXY, geometria: QgsGeometry) -> float:
    """
    Calcula a distância perpendicular do ponto ao eixo rodoviário.
    
    Args:
        ponto: Ponto a ser consultado
        geometria: Geometria do eixo
    
    Returns:
        Distância em metros
    """
    ponto_geom = QgsGeometry.fromPointXY(ponto)
    return ponto_geom.distance(geometria)


# ============================================
# FUNÇÃO PRINCIPAL - CONSULTA
# ============================================

def consultar_coordenadas(x: float, y: float, zona: int) -> Optional[Dict[str, Any]]:
    """
    Executa consulta completa de coordenadas nos shapefiles.
    Verifica: FXD (polígonos), Shape (linhas do eixo), Municípios
    
    Args:
        x: Coordenada X (Este) em metros
        y: Coordenada Y (Norte) em metros
        zona: Zona UTM (23 ou 24)
    
    Returns:
        Dicionário com resultados ou None se não encontrado
    """
    # Validações
    if not validar_coordenadas(x, y, zona):
        return None
    
    # Criar ponto de consulta
    epsg = ZONA_EPSG[zona]
    crs = QgsCoordinateReferenceSystem(f"EPSG:{epsg}")
    ponto = QgsPointXY(x, y)
    ponto_geom = QgsGeometry.fromPointXY(ponto)
    
    print(f"\n📍 Consultando coordenadas:")
    print(f"   X: {x}")
    print(f"   Y: {y}")
    print(f"   Zona: {zona} (EPSG:{epsg})")
    
    # ========================================
    # 1. VERIFICAR SE ESTÁ DENTRO DA FXD (polígono)
    # ========================================
    fxd_info = None
    dentro_fxd = False
    
    fxd_shape = SHAPES_DIR / f"FXD{zona}.shp"
    if fxd_shape.exists():
        print(f"\n🔍 Verificando FXD (Faixa de Domínio)...")
        fxd_layer = QgsVectorLayer(str(fxd_shape), "FXD", "ogr")
        
        if fxd_layer.isValid():
            for feature in fxd_layer.getFeatures():
                if feature.geometry().contains(ponto_geom) or feature.geometry().intersects(ponto_geom):
                    dentro_fxd = True
                    attrs = feature.attributes()
                    fields = [f.name() for f in fxd_layer.fields()]
                    
                    fxd_info = {}
                    for i, field in enumerate(fields):
                        if field.upper() not in ['FID', 'SHAPE_LENG', 'SHAPE_LEN', 'OBJECTID', 'SHAPE_AREA']:
                            fxd_info[field] = attrs[i]
                    
                    print(f"   ✅ Ponto DENTRO da Faixa de Domínio")
                    break
    
    # ========================================
    # 2. BUSCAR MUNICÍPIO
    # ========================================
    municipio = None
    
    munic_shape = SHAPES_DIR / f"municipios{zona}.shp"
    if munic_shape.exists():
        print(f"\n🔍 Buscando município...")
        munic_layer = QgsVectorLayer(str(munic_shape), "municipios", "ogr")
        
        if munic_layer.isValid():
            for feature in munic_layer.getFeatures():
                if feature.geometry().contains(ponto_geom):
                    attrs = feature.attributes()
                    fields = [f.name() for f in munic_layer.fields()]
                    
                    for i, field in enumerate(fields):
                        if any(x in field.upper() for x in ['NM_MUN', 'MUNICIPIO', 'MUNIC', 'NOME']):
                            municipio = attrs[i]
                            print(f"   ✅ Município: {municipio}")
                            break
                    break
    
    # ========================================
    # 3. BUSCAR EIXO RODOVIÁRIO MAIS PRÓXIMO
    # ========================================
    shape_shape = SHAPES_DIR / f"shape{zona}.shp"
    if not shape_shape.exists():
        print(f"\n❌ Shapefile shape{zona}.shp não encontrado")
        return None
    
    print(f"\n🔍 Buscando eixo rodoviário mais próximo...")
    
    shape_layer = QgsVectorLayer(str(shape_shape), "shape", "ogr")
    
    if not shape_layer.isValid():
        print(f"   ❌ Erro ao carregar shape{zona}.shp")
        return None
    
    # Buscar feição mais próxima
    resultado_final = None
    menor_distancia = float('inf')
    total_features = shape_layer.featureCount()
    features_processadas = 0
    features_dentro_limite = 0
    distancia_maxima = 200  # Aumentado para 200m
    
    print(f"   Total de feições no shape{zona}: {total_features}")
    
    # Primeiro, coletar TODAS as features para análise de continuidade
    todas_features = []
    fields = [f.name() for f in shape_layer.fields()]
    
    for feature in shape_layer.getFeatures():
        geom = feature.geometry()
        if geom.isEmpty():
            continue
        
        attrs = feature.attributes()
        atributos_dict = {}
        
        for i, field in enumerate(fields):
            atributos_dict[field] = attrs[i]
        
        todas_features.append((geom, atributos_dict))
    
    # Agora processar cada feature para encontrar a mais próxima
    for feature_data in todas_features:
        features_processadas += 1
        geom, atributos_dict = feature_data
        
        # Calcular distância ao eixo
        distancia = calcular_distancia_do_eixo(ponto, geom)
        
        # Filtrar por distância máxima
        if distancia > distancia_maxima:
            # Guardar menor distância para feedback (mesmo fora do limite)
            if distancia < menor_distancia:
                menor_distancia = distancia
            continue
        
        features_dentro_limite += 1
        
        # Buscar campos de KM
        km_inicial = None
        km_final = None
        
        for field, valor in atributos_dict.items():
            field_lower = field.lower()
            if 'km' in field_lower and 'inicial' in field_lower:
                km_inicial = valor
            elif 'km' in field_lower and 'final' in field_lower:
                km_final = valor
        
        if km_inicial is None or km_final is None:
            continue
        
        # Calcular KM exato (passando atributos e todas as features para análise de continuidade)
        km_calculado = calcular_km_no_eixo(geom, ponto, km_inicial, km_final, 
                                           atributos=atributos_dict, 
                                           todas_features=todas_features)
        
        if km_calculado is None:
            continue
        
        # Se é o mais próximo até agora (já passou pelo filtro de distância máxima)
        if resultado_final is None or distancia < resultado_final['distancia_eixo']:
            menor_distancia = distancia
            
            # Montar resultado
            resultado_final = {
                'shapefile': f'shape{zona}',
                'distancia_eixo': distancia,
                'km_inicial': km_inicial,
                'km_final': km_final,
                'km_calculado': km_calculado,
                'dentro_fxd': dentro_fxd,
                'municipio': municipio,
                'attributes': atributos_dict.copy()
            }
            
            # Adicionar atributos da FXD se estiver dentro
            if fxd_info:
                resultado_final['fxd_info'] = fxd_info
    
    print(f"   Feições processadas: {features_processadas}")
    print(f"   Feições dentro do limite (<{distancia_maxima}m): {features_dentro_limite}")
    
    if resultado_final:
        print(f"   ✅ Eixo encontrado - Distância: {resultado_final['distancia_eixo']:.2f}m")
        return resultado_final
    
    print(f"   ❌ Nenhuma feição encontrada dentro do limite de {distancia_maxima}m.")
    if menor_distancia != float('inf'):
        print(f"   ℹ️  Rodovia mais próxima está a {menor_distancia:.2f}m de distância.")
        print(f"   💡 Coordenada pode estar muito longe das rodovias ou em zona incorreta.")
    return None


# ============================================
# EXIBIÇÃO DE RESULTADOS
# ============================================

def exibir_resultado(resultado: Dict[str, Any]) -> None:
    """
    Exibe resultado da consulta de forma formatada.
    
    Args:
        resultado: Dicionário com dados da consulta
    """
    attrs = resultado['attributes']
    fxd_info = resultado.get('fxd_info', {})
    
    # Buscar campos dinamicamente (shape e FXD)
    def buscar_campo(keywords, source='both'):
        """Busca valor por palavras-chave no nome do campo"""
        # Priorizar FXD se estiver dentro
        if source in ['both', 'fxd'] and fxd_info:
            for k in fxd_info.keys():
                if any(kw in k.upper() for kw in keywords):
                    valor = fxd_info[k]
                    if valor not in [None, '', 'NULL', 'null']:
                        return valor
        
        # Buscar no shape
        if source in ['both', 'shape']:
            for k in attrs.keys():
                if any(kw in k.upper() for kw in keywords):
                    valor = attrs[k]
                    if valor not in [None, '', 'NULL', 'null']:
                        return valor
        return None
    
    # Extrair informações (priorizar FXD quando dentro)
    rodovia = buscar_campo(['RODOVIA', 'NOME', 'SIGLA']) or 'N/A'
    cod_sre = buscar_campo(['COD_SRE', 'SRE', 'CODIGO']) or 'N/A'
    jurisdicao = buscar_campo(['JURISDI_C', 'JURISDICAO', 'JURISD', 'ESFERA'])
    largura_fxd = buscar_campo(['TOTAL FXD', 'LARGURA', 'LARG_FXD', 'FXD', 'FAIXA'])
    amparo_legal = buscar_campo(['AMPARO LEG', 'AMPARO', 'LEI', 'LEGAL', 'LEGISL'])
    tipo_pavimento = buscar_campo(['TIPO_DE_RE', 'PAVIMENTO', 'REVESTIMENTO', 'TIPO'])
    
    # Município
    municipio = resultado.get('municipio') or buscar_campo(['MUNICIPIO', 'MUNIC', 'NM_MUN']) or 'N/A'
    
    # Trecho (priorizar FXD)
    local_ini = buscar_campo(['LOCAL_IN_', 'LOCAL_INI', 'INICIO'])
    local_fim = buscar_campo(['LOCAL_FIM', 'LOCAL_FINAL', 'FIM'])
    
    if local_ini and local_fim:
        trecho = f"{local_ini} - {local_fim}"
    else:
        trecho = buscar_campo(['TRECHO', 'DESCRICAO', 'DESC'])
    
    # Status FXD
    dentro_fxd = resultado.get('dentro_fxd', False)
    
    # EXIBIR RESULTADO
    print("\n" + "="*60)
    if dentro_fxd:
        print("⚠️  DENTRO DA FXD")
    else:
        print("✅ FORA DA FXD")
    print("="*60)
    
    # Informações principais
    print(f"RODOVIA:           {rodovia}")
    
    if trecho:
        print(f"TRECHO:            {trecho}")
    
    if jurisdicao:
        print(f"JURISDIÇÃO:        {jurisdicao}")
    
    if largura_fxd:
        print(f"LARGURA FXD:       {largura_fxd}")
    
    if amparo_legal:
        print(f"AMPARO LEGAL:      {amparo_legal}")
    
    print(f"CÓDIGO SRE:        {cod_sre}")
    print(f"MUNICÍPIO:         {municipio}")
    
    if tipo_pavimento:
        print(f"PAVIMENTAÇÃO:      {tipo_pavimento}")
    
    print(f"DISTÂNCIA DO EIXO: {resultado['distancia_eixo']:.2f} m")
    print(f"KM CALCULADO:      {resultado['km_calculado']:.2f} km")
    
    print("="*60)


# ============================================
# MAIN - INTERFACE CLI
# ============================================

def main():
    """Função principal - execução CLI."""
    
    parser = argparse.ArgumentParser(
        description='Consulta coordenadas UTM em shapefiles rodoviários',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s --x 510807 --y 8649627 --zona 24
  %(prog)s -x 496787 -y 8640850 -z 24
        """
    )
    
    parser.add_argument('--x', '-x', type=float, required=True,
                       help='Coordenada X (Este) em metros')
    parser.add_argument('--y', '-y', type=float, required=True,
                       help='Coordenada Y (Norte) em metros')
    parser.add_argument('--zona', '-z', type=int, required=True,
                       choices=[23, 24],
                       help='Zona UTM (23 ou 24)')
    
    args = parser.parse_args()
    
    # Inicializar QGIS
    print("🔧 Inicializando PyQGIS...")
    
    QgsApplication.setPrefixPath(QGIS_PATH, True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    
    try:
        # Executar consulta
        resultado = consultar_coordenadas(args.x, args.y, args.zona)
        
        if resultado:
            exibir_resultado(resultado)
            exit_code = 0
        else:
            print("\n❌ Consulta sem resultados.")
            exit_code = 1
    
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        exit_code = 2
    
    finally:
        # Finalizar QGIS
        qgs.exitQgis()
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
