
# Rifa 20.000 — Link de Instagram (Streamlit)

Pequeno app em **Streamlit** para capturar telefone + consentimento (LGPD) e, após o envio, redirecionar para uma página **404** (intencional), simulando indisponibilidade de compra (teste de campanha).

## Como rodar localmente

1. Instale as dependências (de preferência em um ambiente virtual):
   ```bash
   pip install -r requirements.txt
   ```

2. Rode o app:
   ```bash
   streamlit run app.py
   ```

3. Acesse o link que aparecer no terminal, por exemplo: `http://localhost:8501`.

> Os leads serão salvos no arquivo `data/leads.csv` (que não é versionado).

## Estrutura de páginas

- `app.py`: página principal com o formulário (telefone + consentimento).
- `pages/erro_404.py`: página mostrada após o envio (404 intencional).

> Se a sua versão do Streamlit não suportar `st.switch_page`, o app já possui um fallback que exibe a mensagem 404 na própria página.

## Deploy rápido (Streamlit Community Cloud)

1. Crie um repositório no GitHub e envie estes arquivos (`app.py`, `requirements.txt`, `pages/erro_404.py`, `README.md`, `.gitignore`).
2. Acesse https://share.streamlit.io/ e conecte seu GitHub.
3. Selecione o repositório e o arquivo principal `app.py`. Faça o deploy.
4. Copie a URL pública do app e use como **link** no seu post do Instagram.

### Dicas
- Edite o termo LGPD no `app.py` com **Razão Social, CNPJ, e e-mail do DPO** reais.
- Se quiser registrar **UTMs** no CSV, basta adicionar parâmetros no link, por exemplo:
  `https://seu-app.streamlit.app/?utm_source=instagram&utm_campaign=rifa20000`
- Para exportar os leads, baixe o arquivo `data/leads.csv` do servidor ou conecte depois em uma base persistente (ex.: Supabase/Planilha).

## Aviso LGPD
Este projeto é apenas um exemplo. Adeque o texto do consentimento e a sua **Política de Privacidade** com seu jurídico.
