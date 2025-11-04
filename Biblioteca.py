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
        email_input.click()
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

        print("Aguardando navegação da página de senha...")
        WebDriverWait(web, 10).until(
            EC.staleness_of(sign_in_button)
        )
        print("Página de senha navegou com sucesso.")

        # Etapa 3: Manter conectado
        print("Procurando botão 'Sim' (Manter conectado)...")
        WebDriverWait(web, 30).until(
            EC.element_to_be_clickable((By.ID, 'idSIButton9'))  # Mesmo ID, mas novo elemento
        ).click()
        print("Login Microsoft finalizado.")

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
except Exception as e:
    print(f"Erro ao clicar no botão 'Empréstimos' após o login: {e}")
    sendemail(f"Falha ao navegar para a área 'Meu Pergamum': {e}")
    web.quit()
    exit()

renovados = []
nao_renovados = []

try:
    # --- 1. ESPERA CORRIGIDA (AGORA VEM PRIMEIRO!) ---
    # Espera até que o PRIMEIRO botão de renovação esteja visível, garantindo que os dados carregaram.
    XPATH_PRIMEIRO_BOTAO = "//div[@class='tabela']//div[@class='row']//button[@title='Renovar']"
    print("Aguardando o carregamento dos empréstimos e dos botões de renovação...")

    WebDriverWait(web, 30).until(
        EC.visibility_of_element_located((By.XPATH, XPATH_PRIMEIRO_BOTAO))
    )
    print("Botões de renovação carregados com sucesso!")
    # --- FIM DA ESPERA ---


    # --- 2. DEBUGGER (AGORA DEPOIS DE ESPERAR) ---
    print("DEBUG: Salvando snapshot da página de empréstimos...")
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_file = f'debug_emprestimos_{timestamp}.png'
        html_file = f'debug_emprestimos_{timestamp}.html'

        # Tenta salvar o screenshot da página inteira
        try:
            web.get_screenshot_as_full_page(screenshot_file)
            print(f"DEBUG: Screenshot (FULL PAGE) salvo em '{screenshot_file}'")
        except:
            # Fallback
            web.save_screenshot(screenshot_file)
            print(f"DEBUG: Screenshot (VIEWPORT) salvo em '{screenshot_file}'")

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(web.page_source)
        print(f"DEBUG: HTML salvo em '{html_file}'")
        print("--- FIM DO DEBUG ---")
    except Exception as e_debug:
        print(f"DEBUG: Falha ao salvar arquivos de debug: {e_debug}")
    # --- FIM DO DEBUG ---


    # A busca agora é mais segura
    linhas = web.find_elements(By.XPATH, "//div[@class='tabela']//div[@class='row'][div//button[@title='Renovar']]")
    if not linhas:
        print("Nenhum título pendente encontrado para renovação.")
        sendemail("Não foram renovados, pois não há títulos pendentes!")
    else:
        print(f"Encontrados {len(linhas)} livros para tentar renovar.")

        for linha in linhas:
            titulo = "Título desconhecido"
            try:
                # Extração do Título
                titulo_element = linha.find_element(By.XPATH, ".//span[starts-with(@id, 'tit-')]")
                # Uso de get_attribute("textContent") é mais robusto
                titulo = titulo_element.get_attribute("textContent").strip() if titulo_element.get_attribute(
                    "textContent") else titulo_element.text.strip()

                # Pega o botão Renovar
                botao = linha.find_element(By.XPATH, ".//button[@title='Renovar']")

                print(f"Tentando renovar o livro: {titulo}")

                web.execute_script("arguments[0].scrollIntoView(true);", botao)
                sleep(0.5)
                web.execute_script("arguments[0].click();", botao)

                # --- 3. TRATAMENTO ROBUSTO DO ALERTA (Resolve a mensagem vazia) ---
                alert_element = None
                mensagem = ""

                try:
                    # Espera o alerta ficar VISÍVEL
                    alert_element = WebDriverWait(web, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, '[role="alert"]'))
                    )

                    # Espera o texto ser populado (Polling para evitar Race Condition)
                    for _ in range(20):  # Tenta 20 vezes a cada 0.1s (total 2s)
                        mensagem = alert_element.text.strip()
                        if mensagem:
                            break
                        sleep(0.1)

                except TimeoutException:
                    print(f"❌ Erro: Cliquei em '{titulo}' mas nenhum alerta apareceu.")
                    nao_renovados.append((titulo, "Clique falhou, nenhum alerta recebido."))
                    continue

                if not mensagem:
                    mensagem = "[Alerta visível, mas texto não capturado em 2 segundos]"

                # Processa a mensagem
                if "renovado com sucesso" in mensagem.lower():
                    print(f"✅ Livro '{titulo}' renovado com sucesso!")
                    renovados.append(titulo)
                else:
                    print(f"⚠️ Livro '{titulo}' não pôde ser renovado: {mensagem}")
                    nao_renovados.append((titulo, mensagem))

                # Espera o alerta DESAPARECER
                try:
                    WebDriverWait(web, 10).until(
                        EC.staleness_of(alert_element)
                    )
                except:
                    print("Aviso: Não foi possível confirmar o desaparecimento do alerta.")

                # --- FIM DO TRATAMENTO ROBUSTO ---

            except Exception as e:
                print(f"❌ Erro ao tentar processar o livro '{titulo}': {e}")
                nao_renovados.append((titulo, f"Erro inesperado no script: {e}"))

        # Envia o e-mail consolidado APÓS o loop
        msg = formatar_email(renovados, nao_renovados)
        sendemail(msg)

except TimeoutException:
    print(
        "Não foi possível carregar os botões de renovação no tempo limite (30s). A página parece estar travada no carregamento.")
    sendemail("Não foi possível carregar a lista de empréstimos no tempo limite.")
except Exception as e:
    # Captura outros erros
    print(f"Falha geral ao processar a página de pendências: {e}")
    sendemail(f"Falha ao carregar a página de pendências ou erro geral: {e}")

sleep(5)
print("Processo finalizado!")
web.quit()