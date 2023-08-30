from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from time import sleep

# Variáveis de coordenadas latitude e longitude
nLatitude = '381863'
nLongitude = '8043963'

# Abrindo o site no Chrome
driver = webdriver.Chrome()
driver.get('http://sider.derba.ba.gov.br/portalfxd/abrirConsultaCoordenada.do')
driver.set_window_size(1024, 768)

# Selecionando Datum e zona
dropdownDatum = driver.find_element(By.NAME, "cdSistcoordenada")
opDatum = Select(dropdownDatum)
opDatum.select_by_visible_text('SIRGAS_UTM_zona_24S')

# Colocando coordenadas latitude e longitude
campoLat = driver.find_element(By.NAME, "vlXcoord")
campoLat.send_keys(nLatitude)

campoLong = driver.find_element(By.NAME, "vlYcoord")
campoLong.send_keys(nLongitude)

# Clicando em consultar
btnConsultar = driver.find_element(By.XPATH, "//span[@class='spwButtonMain']")
btnConsultar.click()

# Extraindo informações de Rodovia, Trecho e Km
rodovia = driver.find_element(By.NAME, "sgRodovia")
trecho = driver.find_element(By.NAME, "nmTrecho")
km = driver.find_element(By.NAME, "vlKm")

print("Rodovia:", rodovia.get_attribute('value'))
print("Trecho:", trecho.get_attribute('value'))
print("Km:", km.get_attribute('value'))

driver.quit()