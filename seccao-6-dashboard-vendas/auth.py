import streamlit as st
from utils import load_all_css
st.markdown(load_all_css(), unsafe_allow_html=True)
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# ==============================
# \U0001F465 CONFIGURAÇÃO DE USUÁRIOS
# ==============================

USUARIOS = {
    "admin": "1234",
    "bruno": "1234"
}

# ==============================
# \U0001F512 FUNÇÃO DE LOGIN
# ==============================

def login():

    if st.session_state.get("autenticado"):
        return True

    # Centraliza usando colunas
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown(
            "<h2 class='login-title'>\U0001F512 Login</h2>",
            unsafe_allow_html=True
        )

        with st.form("login_form", clear_on_submit=False):

            usuario = st.text_input("\U0001F464 Usuário")
            senha = st.text_input("\U0001F511 Senha", type="password")

            submitted = st.form_submit_button("Entrar", key="login_button")

            if submitted:
                if usuario in USUARIOS and USUARIOS[usuario] == senha:
                    st.session_state.autenticado = True
                    st.session_state.usuario = usuario
                    st.rerun()
                else:
                    st.error("\U0000274C Usuário ou senha inválidos")

        st.markdown('</div>', unsafe_allow_html=True)

    return False



# ==============================
# \U0001F6AA FUNÇÃO DE LOGOUT
# ==============================

def logout():

    st.sidebar.write(
        f"\U0001F464 Usuário logado: "
        f"**{st.session_state.get('usuario', '')}**"
    )

    if st.sidebar.button("\U0001F6AA Sair"):
        st.session_state.autenticado = False
        st.session_state.usuario = None
        st.rerun()


def verificar_login():
    if not st.session_state.get("autenticado", False):
        st.switch_page("app.py")
        st.stop()