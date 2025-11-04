import smtplib
import emoji
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.common import WebDriverException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from time import sleep
import os
from dotenv import load_dotenv
import random

# --- OPÇÕES ANTI-BOT ---
opcoes = webdriver.ChromeOptions()

# 1. Adiciona um User-Agent "humano"
opcoes.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

# 2. Desativa a flag "navigator.webdriver"
opcoes.add_experimental_option("excludeSwitches", ["enable-automation"])
opcoes.add_experimental_option("useAutomationExtension", False)

opcoes.add_argument("--window-size=1920,1080")
opcoes.add_argument("--no-sandbox")
opcoes.add_argument("--disable-dev-shm-usage")
opcoes.add_argument("--disable-gpu")
opcoes.add_argument("--headless=new")
opcoes.add_argument('--lang=pt-BR')

# --- FIM DAS OPÇÕES ANTI-BOT ---

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
    email_envio["From"] = remetente
    email_envio["To"] = remetente
    email_envio["Subject"] = emoji.emojize(f":books: Renovação Livros - {hoje} :books:")

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


# --- INÍCIO DO FLUXO PRINCIPAL ---
web = webdriver.Chrome(options=opcoes)
web.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
print("WebDriver iniciado e configurações anti-bot aplicadas.")

try:
    web.get(URL)
    print("Página de login aberta.")
    sleep(random.uniform(1.0, 3.0))
except WebDriverException as e:
    print(f"Erro ao acessar o site: {e}")
    sendemail("Não foi possível acessar o site da UCB 📵")
    web.quit()
    exit()

try:
    WebDriverWait(web, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    try:
        WebDriverWait(web, 5).until_not(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.vp-pop-up'))
        )
    except:
        print("Popup de vídeo ainda visível, removendo com JS...")
        web.execute_script("""
            const pop = document.querySelector('.vp-pop-up');
            if (pop) pop.remove();
        """)
        sleep(random.uniform(0.5, 1.0))

    elemento_login = WebDriverWait(web, 30).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="pergamum"]/div[2]/div/div[1]/div/div[1]/div/div[2]/div[2]/form/div[1]/div[2]/div'))
    )
    web.execute_script("arguments[0].scrollIntoView(true);", elemento_login)
    sleep(random.uniform(0.5, 1.5))
    elemento_login.click()
    print("Clique no botão 'Comunidade Acadêmica' realizado.")

except Exception as e:
    print(f"Erro ao tentar clicar no botão de login inicial: {e}")
    sendemail(f"Falha no login inicial: {e}")
    web.quit()
    exit()

if not logado(web):
    print("Iniciando fluxo de login da Microsoft...")
    try:
        email_input = WebDriverWait(web, 30).until(EC.element_to_be_clickable((By.ID, 'i0116')))
        email_input.click()
        email_input.send_keys(email)
        email_input.send_keys(Keys.ENTER)
        print("E-mail inserido.")
        sleep(random.uniform(1.0, 2.0))

        pass_input = WebDriverWait(web, 30).until(EC.element_to_be_clickable((By.ID, 'i0118')))
        sign_in_button = WebDriverWait(web, 30).until(EC.element_to_be_clickable((By.ID, 'idSIButton9')))
        pass_input.send_keys(password)
        print("Senha inserida.")
        sign_in_button.click()

        print("Aguardando navegação da página de senha...")
        WebDriverWait(web, 10).until(EC.staleness_of(sign_in_button))
        print("Página de senha navegou com sucesso.")
        sleep(random.uniform(1.0, 2.0))

        print("Procurando botão 'Sim' (Manter conectado)...")
        WebDriverWait(web, 30).until(EC.element_to_be_clickable((By.ID, 'idSIButton9'))).click()
        print("Login Microsoft finalizado.")
        sleep(random.uniform(1.5, 3.0))

    except Exception as e:
        print(f"Erro durante o fluxo de login da Microsoft: {e}")
        sendemail(f"Falha ao tentar logar na conta Microsoft: {e}")
        web.quit()
        exit()
else:
    print("Já estava logado.")

try:
    WebDriverWait(web, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[4]/div[1]/div/button[1]'))
    ).click()
    print("Redirecionado para a página 'Meu Pergamum'.")
    sleep(random.uniform(1.0, 2.0))
except Exception as e:
    print(f"Erro ao clicar no botão 'Empréstimos' após o login: {e}")
    sendemail(f"Falha ao navegar para a área 'Meu Pergamum': {e}")
    web.quit()
    exit()

renovados = []
nao_renovados = []

# --- INÍCIO DO BLOCO DE PROCESSAMENTO DE EMPRÉSTIMOS ---
try:
    SPINNER_XPATH = "(//div[@class='tabela'])[1]//div[@role='status']"
    print("Aguardando o carregamento da lista de 'Títulos pendentes' (max 30s)...")

    try:
        WebDriverWait(web, 30).until(EC.invisibility_of_element_located((By.XPATH, SPINNER_XPATH)))
        print("Carregamento da lista de empréstimos finalizado.")
    except TimeoutException:
        print("ERRO DE CARREGAMENTO: O spinner não desapareceu após 30s.")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_file = f'debug_emprestimos_FALHA_{timestamp}.png'
        html_file = f'debug_emprestimos_FALHA_{timestamp}.html'
        web.save_screenshot(screenshot_file)
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(web.page_source)
        sendemail("Não foi possível carregar a lista de empréstimos no tempo limite (Provável bloqueio de Bot).")
        web.quit()
        exit()

    print("DEBUG: Salvando snapshot da página de empréstimos...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_file = f'debug_emprestimos_{timestamp}.png'
    html_file = f'debug_emprestimos_{timestamp}.html'

    S = lambda X: web.execute_script('return document.body.parentNode.scroll' + X)
    web.set_window_size(S('Width'), S('Height'))
    web.find_element(By.TAG_NAME, 'body').screenshot(screenshot_file)
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(web.page_source)
    print(f"DEBUG: Screenshot (FULL PAGE) salvo em '{screenshot_file}'")
    print(f"DEBUG: HTML salvo em '{html_file}'")
    print("--- FIM DO DEBUG ---")

    print("Iniciando processamento de títulos...")
    LINHAS_XPATH = "//span[starts-with(@id, 'tit-')]"  # cada livro visível
    BOTOES_XPATH = "//button[@title='Renovar']"  # todos os botões de renovação

    titulos = web.find_elements(By.XPATH, LINHAS_XPATH)
    botoes = web.find_elements(By.XPATH, BOTOES_XPATH)

    print(f"Encontrados {len(titulos)} títulos e {len(botoes)} botões de renovação.")

    if not titulos or not botoes:
        sendemail("Nenhum livro foi renovado: não foram encontrados títulos ou botões 'Renovar'.")
    else:
        for i, titulo_element in enumerate(titulos):
            titulo = titulo_element.text.strip() or "Título não identificado"
            print(f"[{i + 1}] Tentando renovar: {titulo}")

            # Garante que o índice exista
            if i >= len(botoes):
                print(f"⚠️ Sem botão correspondente para '{titulo}'.")
                nao_renovados.append((titulo, "Sem botão correspondente."))
                continue

            botao = botoes[i]

            try:
                web.execute_script("arguments[0].scrollIntoView(true);", botao)
                sleep(random.uniform(0.8, 1.2))
                web.execute_script("arguments[0].click();", botao)
                print(f"🖱️ Clique no botão 'Renovar' executado para '{titulo}'.")

                # Espera o alerta aparecer
                mensagem = ""
                try:
                    alert_element = WebDriverWait(web, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, '[role=\"alert\"]'))
                    )
                    for _ in range(20):
                        mensagem = alert_element.text.strip()
                        if mensagem:
                            break
                        sleep(0.1)
                except TimeoutException:
                    print(f"❌ Nenhum alerta apareceu para '{titulo}'.")
                    nao_renovados.append((titulo, "Nenhum alerta após clique."))
                    continue

                if not mensagem:
                    mensagem = "[Alerta visível, mas sem texto]"

                if "renovado com sucesso" in mensagem.lower():
                    print(f"✅ '{titulo}' renovado com sucesso!")
                    renovados.append(titulo)
                else:
                    print(f"⚠️ '{titulo}' não pôde ser renovado: {mensagem}")
                    nao_renovados.append((titulo, mensagem))

                # Espera o alerta sumir
                try:
                    WebDriverWait(web, 10).until(EC.staleness_of(alert_element))
                except:
                    print("Aviso: alerta não desapareceu, continuando...")

            except Exception as e:
                print(f"❌ Erro ao processar '{titulo}': {e}")
                nao_renovados.append((titulo, f"Erro inesperado: {e}"))

        msg = formatar_email(renovados, nao_renovados)
        sendemail(msg)

except Exception as e:
    print(f"Falha geral ao processar a página de pendências: {e}")
    sendemail(f"Falha ao carregar a página de pendências ou erro geral: {e}")

sleep(5)
print("Processo finalizado!")
web.quit()
