from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import geopandas as gpd
from shapely.geometry import Point
from tkinter import *
import customtkinter
import tkinter as ttk
from PIL import Image, ImageTk
import pandas as pd
from time import sleep

cor1 = '#ffffff' #branco
cor2 = '#f5f5f5' #off white
cor3 = '#059de3' #azul claro
cor4 = '#012c40' #azul escuro
cor5 = '#000000' #preto

root = Tk()
root.title('Consulta de Coordenadas')
root.geometry('720x480')
root.configure(bg=cor1)
#root.attributes('-alpha',0.95)

ldEsq = Frame(root, width=360, height=480, pady=0, padx=0, bg=cor3)
ldEsq.place(x=0, y=0)

titulo = Label(ldEsq, text='Consulta de Coordenadas', bg=cor3, fg=cor1, pady=50, padx=0, relief=FLAT, font= ('Calibre', 15))
titulo.place(x=60, y=50)

titulo_lat = Label(ldEsq, text='Digite Latitude:', bg=cor3, fg=cor2, pady=0, padx=0, relief=FLAT, font=('Calibre', 10), anchor='center')
titulo_lat.place(x=60, y=150)

entry_lat = Entry(ldEsq, width=32, font=('Calibre', 10))
entry_lat.place(x=60, y=170)

titulo_long = Label(ldEsq, text='Digite Longitude:', bg=cor3, fg=cor2, pady=0, padx=0, relief=FLAT, font=('Calibre', 10), anchor='center')
titulo_long.place(x=60, y=210)

entry_long = Entry(ldEsq, width=32, font=('Calibre', 10))
entry_long.place(x=60, y=230)

btn_consulta = Button(text='Consultar', font=('Calibre', 10))
btn_consulta.place(x=145, y=300)

ldDir = Frame(root, width=360, height=480, pady=0, padx=0, bg=cor1)
ldDir.place(x=360, y=0)


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
    df = pd.read_excel("C:\\Users\\savio.silva\\Documents\\consulta coordenadas\\ConsultaCoordenadasSIT\\sreCompleto.xlsx")

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


#btnConsultar = Button(text='Consultar', command=click get_coordinates)

root.mainloop()