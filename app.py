from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import geopandas as gpd
from tkinter import *
import tkinter as ttk
import pandas as pd
from time import sleep

# Tela principal
janela = Tk()
# Titulo da janela
janela.title('Consulta de Coordenadas')
# Dimensões da janela (largura x altura)
#janela.geometry('800x600')
janela.configure(bg='white')


def get_coordinates(latitude, longitude, zona):
    # Abrindo o site no Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")  # Remove do console a mentagem "DevTools listening on ws://127.0.0.1:58958/devtools/browser..."
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('http://sider.derba.ba.gov.br/portalfxd/abrirConsultaCoordenada.do')
    
    # Selecionando Datum e zona
    dropdownDatum = driver.find_element(By.NAME, "cdSistcoordenada")
    opDatum = Select(dropdownDatum)
    
    if zona == "23":
        opDatum.select_by_visible_text('SIRGAS_UTM_zona_23S')
    elif zona == "24":
        opDatum.select_by_visible_text('SIRGAS_UTM_zona_24S')

    # Aguardar até que o campo de latitude esteja clicável
    campoLat = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "vlXcoord"))
    )
    campoLat.send_keys(latitude)

    campoLong = driver.find_element(By.NAME, "vlYcoord")
    campoLong.send_keys(longitude)

    # Clicando em consultar
    btnConsultar = driver.find_element(By.XPATH, "//span[@class='spwButtonMain']")
    btnConsultar.click()

    # Extraindo informações de Rodovia, Trecho e Km
    rodovia = driver.find_element(By.NAME, "nmRodovia")
    trecho = driver.find_element(By.NAME, "nmTrecho")
    km = driver.find_element(By.NAME, "vlKm")

    print("\nRodovia:          ", rodovia.get_attribute('value'))
    print("Trecho:           ", trecho.get_attribute('value'))
    print("Km:               ", km.get_attribute('value'))

    # Nome para pesquisar
    nome_pesquisa = trecho.get_attribute('value')

    driver.quit()

    # Carregar a planilha
    df = pd.read_excel("sreCompleto.xlsx")

    # Filtrar as linhas que correspondem ao nome
    filtro = df['TRECHO'] == nome_pesquisa
    linha_encontrada = df.loc[filtro]

    # Verificar se o nome foi encontro
    if not linha_encontrada.empty:
        cod = linha_encontrada['CÓDIGO'].values[0]
        kmi = linha_encontrada['INICIAL'].values[0]
        kmf = linha_encontrada['FINAL'].values[0]
        kmt = linha_encontrada['EXTENÇÃO'].values[0]
        mun = linha_encontrada['MUNICÍPIO'].values[0]
        fxd = linha_encontrada['TOTAL FXD'].values[0]
        amparo = linha_encontrada['AMPARO LEGAL'].values[0]
        juris = linha_encontrada['JURISDIÇÃO'].values[0]
        print(f"Código SRE:       {cod}")
        print(f"Km Inicial:       {kmi}")
        print(f"Km Final:         {kmf}")
        print(f"Extenção Total:   {kmt}")
        print(f"Município:        {mun}")
        print(f"Jurisdição:       {juris}")
        print(f"Largura da FXD:   {fxd}")
        print(f"Amparo Legal:     {amparo}")
    else:
        print(f"Trecho {nome_pesquisa} não encontrado no SRE.")

# Loop contínuo
while True:
    # Solicita entrada de latitude e longitude
    nLatitude = input("Digite a latitude: ")
    nLongitude = input("Digite a longitude: ")
    nZona = input("Digite a zona (23 ou 24): ")

    # Chama a função para obter as coordenadas
    get_coordinates(nLatitude, nLongitude, nZona)

    continuar = input("\n\nDeseja continuar? (s/n): ")
    if continuar.lower() != "s":
        break  # Sair do loop se a resposta não for 's'


# Loop principal
janela.mainloop()