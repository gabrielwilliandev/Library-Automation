import smtplib
import emoji
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from time import sleep
import os
from dotenv import load_dotenv


opcoes = webdriver.ChromeOptions()
opcoes.add_argument('--headless=new')
load_dotenv()

email = os.getenv("UCB_EMAIL")
password = os.getenv("UCB_PASS")

MEU_PERGAMUM = 'https://ucb.pergamum.com.br/meupergamum'

URL = 'https://ucb.pergamum.com.br/login?redirect=%2F'

def nome() -> str:
    usuario = os.getenv("UCB_EMAIL").split("@")[0]

    partes = usuario.split(".")

    nome = " ".join(p.capitalize() for p in partes)
    return nome

def sendemail(msg):

    smtp_server = "smtp.office365.com"
    port = 587
    remetente = os.getenv("UCB_EMAIL")
    senha = os.getenv("UCB_PASS")
    hoje = datetime.now().strftime("%d/%m/%Y")

    email_envio = MIMEMultipart()
    email_envio["From"] = os.getenv("UCB_EMAIL")
    email_envio["To"] = os.getenv("UCB_EMAIL")
    email_envio["Subject"] = emoji.emojize(":books: Renovação Livros - {} :books:".format(hoje))

    corpo = f"""  
    <p>Olá, {nome()}! 😄</p>

    <p>Os seus livros {msg} </p>
    <p>At.te, BoBot 🤖 | {hoje}! </p>
    """
    email_envio.attach(MIMEText(corpo, "html"))
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(remetente, senha)
            server.send_message(email_envio)
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

def renovados(foram):
    if foram:
        return "foram renovados hoje! 😁"
    else:
        return "não foram renovados hoje! 😔"

def logado(web):
    try:
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[4]/div[1]/div/button[1]'))
        )
        return True
    except:
        return False

def pendente(web):
    try:
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="mp-root"]/div/div[1]/div[5]/div/div[2]/div[2]/div/div[1]/div[1]/h5'))
        )
        return True
    except:
        return False

web = webdriver.Chrome(options = opcoes)

try:
    web.get(URL)
except WebDriverException as e:
    print(f"Erro ao acessar o site: {e}")
    # Aqui você pode enviar e-mail ou encerrar o script
    sendemail("não foram possíveis de renovar. O site pode estar fora do ar. 📵")
    web.quit()
    exit()
web.maximize_window()

try:
    element = WebDriverWait(web, 50).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="pergamum"]/div[2]/div/div[1]/div/div'
                                              '[1]/div/div[2]/div[2]/form/div[1]/div[2]/div'))
    )
except:
    web.quit()


sleep(3)

web.find_element(By.XPATH, '//*[@id="pergamum"]/div[2]/div/div[1]/div/div'
                               '[1]/div/div[2]/div[2]/form/div[1]/div[2]/div').click()
if logado(web):
    print("Logado!")

if not logado(web):

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

    print("Logado com sucesso!")

WebDriverWait(web, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[4]/div[1]/div/button[1]')))
web.find_element(By.XPATH, '//*[@id="content"]/div[4]/div[1]/div/button[1]').click()

web.get(MEU_PERGAMUM)
sleep(3)
if pendente(web):
    print("Existem títulos pendentes!")

    botoes = web.find_elements(By.XPATH, "//button[@title='Renovar']")
    foram = False

    for botao in botoes:
        try:
            botao.click()
            WebDriverWait(web, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[role="alert"]'))
            )
            mensagem = web.find_element(By.CSS_SELECTOR, '[role="alert"]').text
            if "renovado com sucesso!" in mensagem.lower():
                print("Livro renovado!")
                foram = True

            else:
                print("Livro não pôde ser renvoado hoje!")
        except Exception as e:
            print(f"Erro ao tentar renovar: {e}")
            foram = False
    msg = renovados(foram)
    sendemail(msg)

else:
    print("Nenhum Título pendente!")
    sendemail("Não foram renovados, pois não há títulos pendentes!")

sleep(5)
print("Processo finalizado!")
web.quit()

