# BoBot - Automação de Renovação de Livros do Pergamum 📚🤖

BoBot é um script em **Python** que automatiza a renovação de livros da plataforma **Pergamum** da UCB. Ele verifica se há títulos pendentes e tenta renová-los automaticamente. Ao final, envia um e-mail com o status da renovação. O script pode ser executado localmente ou via **GitHub Actions**, permitindo automação diária sem intervenção manual.

---

## 🚀 Funcionalidades

* ✅ Verifica se existem livros com títulos pendentes
* ✅ Realiza a renovação automática dos livros
* ✅ Envia notificação por e-mail sobre o status da renovação
* ✅ Suporta execução **local** ou via **GitHub Actions**
* ✅ Executa em modo **headless** (Chrome sem interface gráfica) para automação segura

---

## 🧰 Tecnologias utilizadas

* Python 3.10+
* Selenium
* dotenv (para gerenciar credenciais)
* emoji (para logs e e-mails)
* smtplib / email.mime (para envio de e-mails)
* GitHub Actions (para execução automática)

---

## ⚙️ Configuração

### Instalar dependências

```bash
pip install selenium python-dotenv emoji webdriver-manager
```

### Configurar variáveis de ambiente (execução local)

Crie um arquivo `.env` na raiz do projeto com:

```bash
UCB_EMAIL=seu_email@ucb.com.br
UCB_PASS=sua_senha
```

> ⚠️ **Atenção:** As credenciais não devem ser versionadas. Se for usar no GitHub Actions, adicione-as como **Secrets** do repositório (`UCB_EMAIL` e `UCB_PASS`).

---

## 💻 Como rodar localmente

```bash
python Biblioteca.py
```

O script realizará as seguintes ações:

1. Acessa o site do Pergamum
2. Realiza login com suas credenciais
3. Verifica títulos pendentes
4. Renova os livros automaticamente (se possível)
5. Envia e-mail com o status da renovação

---

## ☁️ Execução via GitHub Actions

O script pode ser automatizado diariamente usando **GitHub Actions**. Um workflow funcional (`.github/workflows/renovacao.yml`)

> 🕒 O GitHub Actions usa fuso **UTC**, então o cron `0 20 * * *` executa às **17:00 de Brasília**.

---

## 🧱 Estrutura do projeto

```plaintext
.
├── Biblioteca.py        # Script principal
├── .env                 # Credenciais (não subir para o repositório)
├── README.md            # Este arquivo
└── .github/workflows/   # Workflow do GitHub Actions
```

---

## 🧾 Logs e mensagens possíveis

* `Nenhum título pendente encontrado` → Nenhum livro disponível para renovação
* `Livro renovado com sucesso` → Renovação concluída com êxito
* `Não foi possível renovar` → O limite de renovações pode ter sido atingido
* `Erro de login` → Credenciais incorretas ou instabilidade do site

---

## 💡 Dicas e observações

* O script roda em **modo headless**, sem interface gráfica.
* No GitHub Actions, o Chrome é instalado automaticamente.
* O idioma e tamanho da janela são configurados via opções `--lang=pt-BR` e `--window-size=1920,1080`.
* Utilize `webdriver-manager` para garantir compatibilidade entre Chrome e ChromeDriver.
* A UCB exige renovação constante da senha do email universitário, ao atualizar a senha, atualize a senha nos Secrets ou no .env.
---

## 👨‍💻 Autor

Desenvolvido por **Gabriel Willian** 🤖
Sugestões e melhorias são bem-vindas! Abra uma *issue* no repositório ou envie um *pull request*.
