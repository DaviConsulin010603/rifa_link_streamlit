import streamlit as st
import pandas as pd
import os, json

st.set_page_config(page_title="🔒 Admin — Rifa 20.000", page_icon="🔒", layout="wide")
st.title("🔒 Admin — Leads da Rifa 20.000")

# --- Senha vinda do secrets.toml ---
correct = st.secrets.get("admin_password", "")

# Guarda estado de login
if "authed" not in st.session_state:
    st.session_state.authed = False

# Form de login com botão
with st.form("login_form", clear_on_submit=False):
    pwd = st.text_input("Senha do admin", type="password")
    ok = st.form_submit_button("Entrar")

if ok:
    if not correct:
        st.error("Senha do admin não configurada. Crie .streamlit/secrets.toml com admin_password.")
    elif pwd == correct:
        st.session_state.authed = True
        st.success("Autenticado!")
    else:
        st.error("Senha incorreta.")

# Bloqueia se não logado
if not st.session_state.authed:
    st.info("Digite a senha e clique **Entrar** para ver os leads.")
    st.stop()

# Botão de sair
with st.sidebar:
    if st.button("Sair do admin"):
        st.session_state.authed = False
        st.rerun()

# ---- Dados -------------------------------------------------------------
path = "data/leads.csv"
if not os.path.exists(path):
    st.warning("Ainda não há leads cadastrados.")
    st.stop()

df = pd.read_csv(path)

def parse_params(s):
    try:
        d = json.loads(s) if isinstance(s, str) else {}
        if isinstance(d, dict):
            out = {}
            for k, v in d.items():
                out[k] = v[0] if isinstance(v, list) and v else v
            return out
    except Exception:
        pass
    return {}

utms = df["query_params"].apply(parse_params)
df["utm_source"]   = utms.apply(lambda d: d.get("utm_source", ""))
df["utm_campaign"] = utms.apply(lambda d: d.get("utm_campaign", ""))
df["utm_medium"]   = utms.apply(lambda d: d.get("utm_medium", ""))

col1, col2 = st.columns([2,1])
with col1:
    q = st.text_input("Buscar (telefone, id, UTM...)", "")
with col2:
    st.metric("Total de leads", len(df))

if q:
    ql = q.lower()
    df = df[df.apply(lambda r: ql in str(r.values).lower(), axis=1)]

st.dataframe(df, use_container_width=True)

st.download_button(
    "Baixar CSV filtrado",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="leads_filtrados.csv",
    mime="text/csv",
)
