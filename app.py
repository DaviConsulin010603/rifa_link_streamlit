import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
import re, csv, os, uuid, json

st.set_page_config(page_title="Rifa 20.000 — Cadastro", page_icon="🎟️", layout="centered")

st.title("🎟️ RIFA R$20.000 EM PRÊMIO — Cadastro rápido")
st.write("sua chance de ganhar mais de 20 mil em dinheiro")

def normalize_phone_br(raw: str):
    digits = re.sub(r"\D", "", raw or "")
    if len(digits) == 11:   # DDD + 9 dígitos (celular)
        return f"+55{digits}"
    if len(digits) == 10:   # DDD + 8 dígitos (fixo)
        return f"+55{digits}"
    if digits.startswith("55") and len(digits) in (12, 13):
        return f"+{digits}"
    return None

def get_query_params():
    try:
        params = st.query_params  # st>=1.31
        return {k: v for k, v in params.items()}
    except Exception:
        try:
            return st.experimental_get_query_params()
        except Exception:
            return {}

with st.form("lead_form", clear_on_submit=False):
    phone = st.text_input("Telefone (WhatsApp)", placeholder="(11) 9 8765-4321")
    consent = st.checkbox("Li e aceito o **Termo de Consentimento LGPD** para receber mensagens por WhatsApp/SMS/telefone.")

    with st.expander("Ver termo de consentimento"):
        st.markdown(
            """
**Controlador:** *ITSPLAY*, .  
**Finalidade:** Enviar comunicações sobre a *Campanha Rifa 20.000* e conteúdos correlatos.  
**Dados coletados:** Telefone (WhatsApp), data/hora do cadastro e parâmetros do anúncio.  
**Base legal:** Consentimento (art. 7º, I); obrigação legal (art. 7º, II e art. 16); legítimo interesse só para prevenção à fraude (oposição possível).  
**Compartilhamento:** Prestadores necessários para o envio de mensagens (ex.: provedores de WhatsApp/SMS).  
**Retenção:** Até 12 meses após o término da campanha ou até revogação do consentimento.  
**Direitos:** acesso, correção, exclusão e revogação a qualquer tempo.    
            """
        )

    submitted = st.form_submit_button("Quero participar")

if submitted:
    norm = normalize_phone_br(phone)
    if not norm:
        st.error("Informe um telefone válido do Brasil (ex.: (11) 9 8765-4321).")
        st.stop()
    if not consent:
        st.error("É necessário aceitar o termo de consentimento para continuar.")
        st.stop()

    os.makedirs("data", exist_ok=True)
    filepath = os.path.join("data", "leads.csv")
    now_br = datetime.now(ZoneInfo("America/Sao_Paulo"))
    params = get_query_params()
    params_json = json.dumps(params, ensure_ascii=False)

    row = {
        "id": str(uuid.uuid4()),
        "created_at": now_br.isoformat(),
        "phone": norm,
        "consent": True,
        "query_params": params_json,
    }

    write_header = not os.path.exists(filepath)
    fieldnames = ["id", "created_at", "phone", "consent", "query_params"]
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow(row)

    try:
        st.switch_page("pages/erro_404.py")
    except Exception:
        st.session_state["_force_404"] = True

if st.session_state.get("_force_404"):
    st.session_state["_force_404"] = False
    st.markdown("# 404 — Página não encontrada")
    st.write("Mas fica tranquilo: **seu cadastro foi recebido com sucesso**. Como este é apenas um teste, a compra ainda não está disponível.")
    st.caption("Você pode fechar esta página agora. Obrigado!")
