# 📚 BoBot – Automação de Renovação de Livros (UCB)

Automatiza a renovação de livros na plataforma **Pergamum** da Universidade Católica de Brasília (UCB) e envia um relatório diário por e‑mail.  
Pode ser executado **localmente** ou de forma **automática via GitHub Actions**.

---

## ⚙️ Funcionalidades

- 🔑 Login automático na conta institucional (Microsoft)
- 🔁 Renovação de todos os títulos pendentes
- 📬 Envio de e‑mail com relatório de sucesso ou falha
- 🤖 Execução automática agendada via GitHub Actions
- 💻 Suporte para execução local (Windows / Linux / GitHub Runner)

---

## 🧰 Tecnologias utilizadas

- **Python 3.10+**
- **Selenium WebDriver**
- **python-dotenv**
- **emoji**
- **smtplib / email.mime**
- **GitHub Actions**


## 🚀 Como configurar e usar

### 1. 🧩 Instalar dependências (para rodar localmente)

```bash
pip install -r requirements.txt
```

Ou, manualmente:

```bash
pip install selenium python-dotenv emoji webdriver-manager
```

---

### 2. 🔐 Criar arquivo `.env` (modo local)

Na raiz do projeto, crie um arquivo chamado `.env` com o conteúdo:

```
UCB_EMAIL=seu_email@ucb.edu.br
UCB_PASS=sua_senha
```

> ⚠️ **Importante:** nunca suba este arquivo para o GitHub.  
> O `.env` deve ser mantido apenas localmente.

---

### 3. ☁️ Configurar no GitHub Actions (modo automático)

Se quiser que o processo rode automaticamente (sem abrir o programa manualmente), basta configurar o **workflow** do GitHub Actions.

#### Passos:

1. Faça **fork** ou **clone** deste repositório para sua conta.
2. Vá em **Settings → Actions → General → Allow all actions** (ativar o Actions).
3. Vá em **Settings → Secrets and variables → Actions → New repository secret**.
4. Adicione os seguintes segredos:

| Nome | Valor |
|------|-------|
| `UCB_EMAIL` | seu e‑mail institucional |
| `UCB_PASS` | sua senha institucional |

5. Vá na aba **Actions** → selecione o workflow → clique em **Run workflow** (para testar manualmente).

Se tudo estiver certo, o GitHub rodará o bot e enviará o e‑mail de relatório.

---

## ⏰ Configurando a frequência de execução (cron)

A automação usa o recurso de **agendamento (`cron`)** do GitHub Actions para definir **quando e com que frequência** o script será executado.

Abra o arquivo:
```
.github/workflows/renovacao.yml
```

Localize o trecho:
```yaml
on:
  schedule:
    - cron: '0 11 * * *'  # Executa todos os dias às 8h (horário de Brasília)
  workflow_dispatch:
```

### ✏️ Como funciona o `cron`
Formato:
```
minuto hora dia-do-mês mês dia-da-semana
```
O GitHub Actions usa **UTC** (3 horas à frente de Brasília).  
Então, para 8h da manhã em Brasília → use **11h UTC**.

---

### 📅 Exemplos de configuração

| Frequência desejada | Cron | Explicação |
|----------------------|------|-------------|
| 🕗 Todos os dias às 8h (Brasília) | `'0 11 * * *'` | Execução diária |
| 📘 A cada 3 dias às 8h (Brasília) | `'0 11 */3 * *'` | A cada 3 dias |
| 📗 1x por semana (segunda‑feira, 8h Brasília) | `'0 11 * * 1'` | Segunda‑feira |
| 📕 1º e 15º de cada mês | `'0 11 1,15 * *'` | Duas vezes por mês |
| 📙 Uma vez por mês (dia 1) | `'0 11 1 * *'` | Mensalmente |


---

## 📬 Relatório por e‑mail

Após cada execução, o bot envia um e‑mail para o endereço configurado contendo:
- ✅ Livros renovados com sucesso  
- ❌ Livros que não puderam ser renovados  
- 📅 Data e hora da execução

---

## 👨‍💻 Autor

**Gabriel Willian**  
Desenvolvido para automatizar a rotina de renovação da biblioteca da UCB.  
Contribuições e melhorias são bem‑vindas!
