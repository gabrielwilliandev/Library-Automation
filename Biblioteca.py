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

opcoes = webdriver.ChromeOptions()

opcoes.add_argument("--window-size=1920,1080")
opcoes.add_argument("--no-sandbox")
opcoes.add_argument("--disable-dev-shm-usage")
opcoes.add_argument("--disable-gpu")
opcoes.add_argument("--headless=new")

# --- PLANO C: User-Agent para melhorar a compatibilidade e renderização ---
opcoes.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
# -------------------------------------------------------------------------

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
        # Espera pelo botão de "Empréstimos" que só aparece logado
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[4]/div[1]/div/button[1]'))
        )
        return True
    except:
        return False


web = webdriver.Chrome(options=opcoes)
print("WebDriver iniciado.")

try:
    web.get(URL)
    print("Página de login aberta.")
except WebDriverException as e:
    print(f"Erro ao acessar o site: {e}")
    sendemail("não foram possíveis de renovar. O site pode estar fora do ar. 📵")
    web.quit()
    exit()

try:
    WebDriverWait(web, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )

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

    elemento_login = WebDriverWait(web, 30).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="pergamum"]/div[2]/div/div[1]/div/div[1]/div/div[2]/div[2]/form/div[1]/div[2]/div'))
    )
    web.execute_script("arguments[0].scrollIntoView(true);", elemento_login)
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
        # Etapa 1: E-mail
        email_input = WebDriverWait(web, 30).until(
            EC.element_to_be_clickable((By.ID, 'i0116'))
        )
        email_input.send_keys(email)
        email_input.send_keys(Keys.ENTER)
        print("E-mail inserido.")

        # Etapa 2: Senha
        pass_input = WebDriverWait(web, 30).until(
            EC.element_to_be_clickable((By.ID, 'i0118'))
        )
        sign_in_button = WebDriverWait(web, 30).until(
            EC.element_to_be_clickable((By.ID, 'idSIButton9'))
        )

        pass_input.send_keys(password)
        print("Senha inserida.")

        sign_in_button.click()
        WebDriverWait(web, 10).until(
            EC.staleness_of(sign_in_button)
        )
        print("Página de senha navegou com sucesso.")

        # Etapa 3: Manter conectado
        print("Procurando botão 'Sim' (Manter conectado)...")
        WebDriverWait(web, 30).until(
            EC.element_to_be_clickable((By.ID, 'idSIButton9'))
        ).click()
        print("Login Microsoft finalizado.")

    except Exception as e:
        print(f"Erro durante o fluxo de login da Microsoft: {e}")
        sendemail(f"Falha ao tentar logar na conta Microsoft: {e}")
        web.quit()
        exit()
else:
    print("Já estava logado.")

# Redirecionamento para a área de empréstimos
try:
    WebDriverWait(web, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[4]/div[1]/div/button[1]'))
    ).click()
    print("Redirecionado para a página 'Meu Pergamum'.")

    # --- PLANO B: ESPERA CUIDADOSA PARA RENDERIZAÇÃO ---
    print("Aguardando 5 segundos para a renderização completa da página de empréstimos...")
    sleep(5)
    # ---------------------------------------------------

except Exception as e:
    print(f"Erro ao clicar no botão 'Empréstimos' após o login: {e}")
    sendemail(f"Falha ao navegar para a área 'Meu Pergamum': {e}")
    web.quit()
    exit()

# --- INÍCIO DO PLANO E: FORÇA BRUTA NO BOTÃO RENOVAR ---
renovados = []
nao_renovados = []

try:
    # 1. Espera **45 segundos** pelo elemento mais importante: qualquer botão 'Renovar'
    print("Tentando localizar botões de renovação (Timeout: 45s)...")
    WebDriverWait(web, 45).until(
        EC.presence_of_element_located((By.XPATH, "//button[@title='Renovar']"))
    )
    print("Pelo menos um botão 'Renovar' foi encontrado no DOM. Coletando todos os botões.")

    # 2. Coleta TODOS os botões de renovação disponíveis
    botoes = web.find_elements(By.XPATH, "//button[@title='Renovar']")

    if not botoes:
        raise TimeoutException("Nenhum botão de renovação encontrado após o carregamento.")

    print(f"Encontrados {len(botoes)} livros para tentar renovar.")

    # 3. Itera e clica usando JavaScript
    for i, botao in enumerate(botoes):
        # Fallback para o título, caso não seja extraído
        titulo = f"Livro {i + 1} (Título não extraído)"
        try:
            # Tenta pegar o título através de JavaScript, mais robusto no Actions
            titulo_script = """
                let row = arguments[0].closest('.row'); // Encontra a div pai da linha
                if (row) {
                    let titleSpan = row.querySelector("span[id^='tit-']");
                    return titleSpan ? titleSpan.textContent.trim() : arguments[1];
                }
                return arguments[1];
            """
            titulo = web.execute_script(titulo_script, botao, titulo)

            print(f"Tentando renovar o livro: {titulo}")

            # Clica diretamente via JavaScript no botão
            web.execute_script("arguments[0].scrollIntoView(true);", botao)
            sleep(0.5)
            web.execute_script("arguments[0].click();", botao)

            # Espera o alerta estar VISÍVEL
            alert_element = WebDriverWait(web, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '[role="alert"]'))
            )
            mensagem = alert_element.text

            if "renovado com sucesso" in mensagem.lower():
                print(f"✅ Livro '{titulo}' renovado com sucesso!")
                renovados.append(titulo)
            else:
                print(f"⚠️ Livro '{titulo}' não pôde ser renovado: {mensagem}")
                nao_renovados.append((titulo, mensagem))

            sleep(1)  # Pausa entre cliques

        except Exception as e:
            print(f"❌ Erro ao tentar processar o livro '{titulo}': {e}")
            nao_renovados.append((titulo, f"Erro inesperado no script: {e}"))

    # Envia o e-mail consolidado
    msg = formatar_email(renovados, nao_renovados)
    sendemail(msg)


except TimeoutException as e:
    # Se o botão não aparecer após 45s
    print(
        f"Falha crítica: O botão 'Renovar' não apareceu após 45 segundos. Assumindo que não há livros para renovar ou que o site falhou na renderização.")
    sendemail(
        "Falha crítica ao tentar renovar os livros. O site pode estar extremamente lento ou falhou na renderização.")

except Exception as e:
    # Erro de estrutura ou qualquer outro erro
    print(f"Erro ao tentar processar a página de renovação: {e}")
    sendemail("Erro ao tentar processar a página de renovação. A estrutura do site pode ter mudado.")

# --- FIM DO PLANO E ---

sleep(5)
print("Processo finalizado!")
web.quit()