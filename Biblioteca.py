from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from time import sleep
import os
from dotenv import load_dotenv

load_dotenv()

email = os.getenv("UCB_EMAIL")
password = os.getenv("UCB_PASS")


MEU_PERGAMUM = 'https://ucb.pergamum.com.br/meupergamum'

URL = 'https://ucb.pergamum.com.br/login?redirect=%2F'


def logado(web):
    html = web.page_source
    return "Sair" in html or "Minha Conta" in html or "Dados Pessoais" in html

def pendente(web):
    livros = web.page_source
    return "Títulos pendentes" in livros


web = webdriver.Chrome()
web.maximize_window()
web.get(URL)

try:
    element = WebDriverWait(web, 50).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="pergamum"]/div[2]/div/div[1]/div/div'
                                              '[1]/div/div[2]/div[2]/form/div[1]/div[2]/div'))
    )
except:
    web.quit()


sleep(3)

if not logado(web):

    web.find_element(By.XPATH, '//*[@id="pergamum"]/div[2]/div/div[1]/div/div'
                               '[1]/div/div[2]/div[2]/form/div[1]/div[2]/div').click()
    WebDriverWait(web,30).until(EC.element_to_be_clickable((By.ID, 'i0116')))
    web.find_element(By.XPATH, '//*[@id="i0116"]').click()
    web.find_element(By.XPATH, '//*[@id="i0116"]').send_keys(email)
    sleep(3)
    web.find_element(By.XPATH, '//*[@id="i0116"]').send_keys(Keys.ENTER)
    sleep(3)
    web.find_element(By.XPATH, '//*[@id="i0118"]').send_keys(password)
    web.find_element(By.XPATH, '//*[@id="i0118"]').send_keys(Keys.ENTER)
    sleep(3)

    try:
        WebDriverWait(web, 30).until(
            EC.element_to_be_clickable((By.ID, 'idSIButton9'))
        )
        web.find_element(By.ID, 'idSIButton9').click()
    except:
        pass


WebDriverWait(web, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[4]/div[1]/div/button[1]')))
web.find_element(By.XPATH, '//*[@id="content"]/div[4]/div[1]/div/button[1]').click()

web.get(MEU_PERGAMUM)
sleep(3)
if pendente(web):
    print("Existem títulos pendentes!")

    botoes = web.find_elements(By.XPATH, "//button[@title='Renovar']")

    for botao in botoes:
        try:
            botao.click()
            WebDriverWait(web, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[role="alert"]'))
            )
            mensagem = web.find_element(By.CSS_SELECTOR, '[role="alert"]').text
            if "Livro renovado!" in mensagem.lower():
                print("Livro renovado!")
            else:
                print("Livro não pode ser renvoado hoje!")
        except Exception as e:
            print(f"Erro ao tentar renovar: {e}")

else:
    print("Nenhum Título pendente!")




sleep(9999)
