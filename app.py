from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl
from time import sleep

def get_coordinates(latitude, longitude, zona):
    # Abrindo o site no Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('http://sider.derba.ba.gov.br/portalfxd/abrirConsultaCoordenada.do')
    #driver.set_window_size(1024, 768)

    # Selecionando Datum e zona
    dropdownDatum = driver.find_element(By.NAME, "cdSistcoordenada")
    opDatum = Select(dropdownDatum)
    
    if zona == "23":
        opDatum.select_by_visible_text('SIRGAS_UTM_zona_23S')
    elif zona == "24":
        opDatum.select_by_visible_text('SIRGAS_UTM_zona_24S')
    
    sleep(1)

    # Colocando coordenadas latitude e longitude
    campoLat = driver.find_element(By.NAME, "vlXcoord")
    campoLat.send_keys(latitude)

    campoLong = driver.find_element(By.NAME, "vlYcoord")
    campoLong.send_keys(longitude)

    # Clicando em consultar
    btnConsultar = driver.find_element(By.XPATH, "//span[@class='spwButtonMain']")
    btnConsultar.click()

    # Verifica se a mensagem de erro foi encontrada
    mensagem_erro = driver.find_elements(By.ID, "spwMensagemId")
    if mensagem_erro:
        print("Nenhuma resposta encontrada:", mensagem_erro[0].text)
    else:
        # Extraindo informações de Rodovia, Trecho e Km
        rodovia = driver.find_element(By.NAME, "nmRodovia")
        trecho = driver.find_element(By.NAME, "nmTrecho")
        km = driver.find_element(By.NAME, "vlKm")

        print("Rodovia:     ", rodovia.get_attribute('value'))
        print("Trecho:      ", trecho.get_attribute('value'))
        print("Km:          ", km.get_attribute('value'))

    driver.quit()

# Loop contínuo
while True:
    # Solicita entrada de latitude
    nLatitude = input("Digite a latitude: ")
    nLongitude = input("Digite a longitude: ")
    nZona = input("Digite a zona (23 ou 24): ")

    # Chama a função para obter as coordenadas
    get_coordinates(nLatitude, nLongitude, nZona)

    continuar = input("Deseja continuar? (s/n): ")
    if continuar.lower() != "s":
        break  # Sair do loop se a resposta não for 's'
