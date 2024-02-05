from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import shutil
import time

# URL do site
url = "https://www2.susep.gov.br/menuestatistica/ses/premiosesinistrosporuftodas.aspx?id=53"

# Inicializar o driver do Selenium usando o Microsoft Edge
driver = webdriver.Edge()

try:
    # Acessar a URL
    driver.get(url)
    time.sleep(3)
    
    periodo = '200301'

    while periodo != '202402':
        # Clicar e incluir a data de início
        campo = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_edInicioPer"]')
        time.sleep(1)
        campo.click()
        time.sleep(1)
        campo.clear()
        time.sleep(3)
        campo.send_keys(periodo)
        time.sleep(3)

        # Clicar em um botão
        campo1 = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_edFimPer"]')
        time.sleep(1)
        campo1.click()
        time.sleep(1)
        campo1.clear()
        time.sleep(3)
        campo1.send_keys(periodo)
        time.sleep(3)

        # Clicar no botão de processar o relatório
        campo2 = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_btnProcessao"]')
        time.sleep(1)
        campo2.click()
        time.sleep(2)
        
        # Aguardar até o elemento aparecer na página
        xpath_campo3 = '//*[@id="ctl00_ContentPlaceHolder1_Button1"]'
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, xpath_campo3)))
        campo3 = driver.find_element(By.XPATH, xpath_campo3)
        time.sleep(2)
        campo3.click()
        time.sleep(2)

        # Clicar em voltar
        campo4 = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_HyperLink1"]')
        time.sleep(2)
        campo4.click() 

        # Substituir o nome do arquivo e mover para a pasta
        diretorio_arquivo = rf"C:\Users\Felipe\Downloads\Exporta.xls"
        novo_diretorio = rf"C:\Users\Felipe\Downloads\susep\{periodo}.xls"
        shutil.move(diretorio_arquivo, novo_diretorio)

        # Incrementar a variável periodo para o próximo ciclo
        # Converte os últimos dois dígitos para um número inteiro
        ano_mes = int(periodo[4:])
        # Incrementa um até 12
        ano_mes += 1
        # Se o mês ultrapassar 12, incrementa o ano e redefine o mês para 1
        if ano_mes > 12:
            ano_mes = 1
            ano = int(periodo[:4]) + 1
            periodo = f"{ano}{ano_mes:02d}"
        else:
            # Atualiza o período
            periodo = periodo[:4] + f"{ano_mes:02d}"

finally:
    # Fechar o navegador ao finalizar
    driver.quit()
