import smtplib
import emoji
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.common import WebDriverException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from time import sleep
import os
from dotenv import load_dotenv


opcoes = webdriver.ChromeOptions()

opcoes.add_argument("--window-size=1920,1080")
opcoes.add_argument("--no-sandbox")
opcoes.add_argument("--disable-dev-shm-usage")
opcoes.add_argument("--disable-gpu")
opcoes.add_argument("--headless=new")
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
    <p>{msg}</p>
    <hr style="border:none; border-top:1px solid #ddd; margin:20px 0;">
    <p style="font-size:14px; color:#777;">
    At.te,<br>
    <b>BoBot 🤖 | {hoje}</b><br>
    Create by Gabriel Willian
    </p>
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

def formatar_email(renovados, nao_renovados):
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
    <h2>Olá, {nome()}! 😄</h2>
    <h2>📚 Relatório de Renovação de Livros | UCB</h2>
    """

    if renovados:
        html += "<h3 style='color:green;'>✅ Livros renovados hoje:</h3><ul>"
        for t in renovados:
            html += f"<li>{t} 📗</li>"
        html += "</ul>"
    else:
        html += "<p>⚠️ Nenhum livro foi renovado hoje!</p>"

    if nao_renovados:
        html += "<h3 style='color:red;'>❌ Não renovados:</h3><ul>"
        for t, motivo in nao_renovados:
            html += f"<li><b>{t}</b> — {motivo}</li>"
        html += "</ul>"

    html += """
    <p>📅 Processo finalizado automaticamente.</p>
    </body>
    </html>
    """

    return html

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

try:
    WebDriverWait(web, 5).until_not(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.vp-pop-up'))
    )
except:
    # Caso continue visível, remove via JavaScript
    web.execute_script("""
        const pop = document.querySelector('.vp-pop-up');
        if (pop) pop.remove();
    """)

# 🔹 Agora sim, pode clicar com segurança
try:
    elemento_login = web.find_element(By.XPATH, '//*[@id="pergamum"]/div[2]/div/div[1]/div/div'
                                                '[1]/div/div[2]/div[2]/form/div[1]/div[2]/div')
    web.execute_script("arguments[0].scrollIntoView(true);", elemento_login)
    elemento_login.click()
    print("Clique inicial realizado com sucesso!")
except Exception as e:
    print(f"Erro ao clicar no botão inicial: {e}")

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

    renovados = []
    nao_renovados = []

    # Captura todas as linhas com botão "Renovar"
    linhas = web.find_elements(By.XPATH, "//div[@class='tabela']//div[@class='row'][div//button[@title='Renovar']]")

    for linha in linhas:
        try:
            # Pega o título do livro dentro da linha
            titulo = linha.find_element(By.XPATH, ".//span[starts-with(@id, 'tit-')]").text

            # Pega o botão Renovar dentro da linha
            botao = linha.find_element(By.XPATH, ".//button[@title='Renovar']")

            print(f"Tentando renovar o livro: {titulo}")

            # Faz o scroll até o botão
            web.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", botao)
            sleep(0.8)

            # Simula um clique real (mousedown + mouseup + click)
            web.execute_script("""
                const el = arguments[0];
                const rect = el.getBoundingClientRect();
                ['mousedown', 'mouseup', 'click'].forEach(evt => {
                    el.dispatchEvent(new MouseEvent(evt, {
                        bubbles: true,
                        cancelable: true,
                        view: window,
                        clientX: rect.x + 5,
                        clientY: rect.y + 5
                    }));
                });
            """, botao)

            # Aguarda a mensagem de feedback aparecer
            WebDriverWait(web, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[role="alert"]'))
            )

            mensagem = web.find_element(By.CSS_SELECTOR, '[role="alert"]').text
            print(f"📩 Mensagem recebida: {mensagem}")

            if "renovado com sucesso" in mensagem.lower():
                print(f"✅ Livro '{titulo}' renovado com sucesso!")
                renovados.append(titulo)
            else:
                print(f"⚠️ Livro '{titulo}' não pôde ser renovado: {mensagem}")
                nao_renovados.append((titulo, mensagem))

            sleep(1.2)  # pausa entre as renovações

        except Exception as e:
            print(f"❌ Erro ao tentar renovar '{titulo}': {e}")
            nao_renovados.append((titulo, "Erro no clique ou resposta inesperada"))

    # Formata e envia o relatório
    msg = formatar_email(renovados, nao_renovados)
    sendemail(msg)

else:
    print("Nenhum título pendente!")
    sendemail("Não foram renovados, pois não há títulos pendentes!")

sleep(5)
print("Processo finalizado!")
web.quit()

