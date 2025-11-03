# BoBot - Automação de Renovação de Livros do Pergamum 📚🤖

BoBot é um script em **Python** que automatiza a renovação de livros da plataforma **Pergamum** da UCB. Ele verifica se há títulos pendentes e tenta renová-los automaticamente. Ao final, envia um e-mail com o status da renovação. O script pode ser executado localmente ou via **GitHub Actions**, permitindo automação diária sem intervenção manual.

---

## Funcionalidades

* ✅ Verifica se existem livros com títulos pendentes
* ✅ Realiza a renovação automática dos livros
* ✅ Envia notificação por e-mail sobre o status da renovação
* ✅ Suporta execução **local** ou via **GitHub Actions**
* ✅ Executa em modo **headless** (Chrome sem interface gráfica) para automação segura

---

## Tecnologias utilizadas

* Python 3.11+
* Selenium
* dotenv (para gerenciar credenciais)
* smtplib / email.mime (para envio de e-mails)
* GitHub Actions (para execução automática)

---

## Configuração

### Instalar dependências

```
pip install selenium python-dotenv emoji
```

### Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com:

```
UCB_EMAIL=seu_email@ucb.com.br
UCB_PASS=sua_senha
```

> **Atenção:** Guarde seu e-mail e senha com segurança. As variáveis de ambiente só são utilizadas caso deseje rodar o código no seu dispositivo local. Caso deseje passar para nuvem, é necessário configurar as variáveis no própio Actions, por exemplo.

---

## Como rodar localmente

```
python Biblioteca.py
```

O script realizará as seguintes ações:

1. Acessa o site do Pergamum
2. Realiza login com suas credenciais
3. Verifica títulos pendentes
4. Renova os livros automaticamente (se possível)
5. Envia e-mail com o status da renovação

---

## Execução via GitHub Actions

O script pode ser automatizado diariamente usando GitHub Actions. Um workflow típico (`.github/workflows/renovacao.yml`) inclui:

```
name: Renovação Pergamum

on:
  schedule:
    - cron: '0 8 * * *' # todos os dias às 8h
  workflow_dispatch:

jobs:
  renovacao:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Configurar Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Instalar dependências
        run: pip install selenium python-dotenv emoji
      - name: Executar script
        run: python Biblioteca.py
        env:
          UCB_EMAIL: ${{ secrets.UCB_EMAIL }}
          UCB_PASS: ${{ secrets.UCB_PASS }}
```

> **Nota:** As credenciais devem ser adicionadas como **Secrets** do repositório no GitHub, evitando expor login e senha.

---

## Estrutura do projeto

```
.
├── Biblioteca.py      # Script principal
├── .env               # Credenciais (não subir para o repositório)
├── README.md          # Este arquivo
└── requirements.txt   # Dependências opcionais
```

---

## Possíveis mensagens e tratamento

* `Nenhum Título pendente!` → Não há livros para renovar
* `Livro renovado!` → Renovação bem-sucedida
* `Erro ao tentar renovar` → Problema durante a renovação (ex.: limite de renovações)
* `Erro ao acessar o site` → O site pode estar fora do ar ou houve problema de conexão

---

## Observações

* O script funciona em **modo headless**, então não é necessário abrir o navegador
* Certifique-se de que o **ChromeDriver** esteja compatível com a versão do seu Chrome
* É recomendado rodar via **GitHub Actions** para automação diária sem precisar de intervenção manual

---

## Contato

Desenvolvido por Gabriel Willian 🤖
Qualquer dúvida ou sugestão, abra uma issue no repositório.
