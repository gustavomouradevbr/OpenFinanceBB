import pandas as pd
import plotly.express as px
import streamlit as st

# 1. Definição de Cores Oficiais (Padrão BB 2026)
BB_AZUL = "#0033A0"
BB_AZUL_ESCURO = "#001F5B"
BB_AMARELO = "#FFCC00"
BB_BRANCO = "#FFFFFF"
BG_CINZA = "#F4F7F9"

# 2. Lógica de Sessão
def init_session_state():
    if "score" not in st.session_state:
        st.session_state.score = 742
        st.session_state.taxa_endividamento = 0.85
        st.session_state.roi = 3500.00
        st.session_state.fluxo_caixa = 2850.00
        st.session_state.analisado = False

# 3. Injeção de CSS
def apply_styles():
    st.markdown(
        f"""
        <style>
            /* Reset e Fonte */
            @import url('https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;700;800&display=swap');
            * {{ font-family: 'Public Sans', sans-serif; }}

            /* Fundo da Página */
            .stApp {{ background-color: {BG_CINZA} !important; }}

            /* Override de variaveis globais do tema no container principal */
            div.stApp,
            [data-testid="stAppViewContainer"],
            [data-testid="stAppViewContainer"] .main {{
                --text-color: {BB_AZUL_ESCURO} !important;
                --primary-text-color: {BB_AZUL_ESCURO} !important;
                color: {BB_AZUL_ESCURO} !important;
                -webkit-text-fill-color: {BB_AZUL_ESCURO} !important;
            }}

            /* FORCA BRUTA DE CONTRASTE NA AREA PRINCIPAL */
            div.stApp .main * {{
                color: {BB_AZUL_ESCURO} !important;
                -webkit-text-fill-color: {BB_AZUL_ESCURO} !important;
            }}

            div.stApp .main input,
            div.stApp .main textarea,
            div.stApp .main select,
            div.stApp .main option,
            div.stApp .main label,
            div.stApp .main span,
            div.stApp .main p,
            div.stApp .main h1,
            div.stApp .main h2,
            div.stApp .main h3,
            div.stApp .main h4,
            div.stApp .main h5,
            div.stApp .main h6 {{
                color: {BB_AZUL_ESCURO} !important;
                -webkit-text-fill-color: {BB_AZUL_ESCURO} !important;
            }}

            div.stApp .main ::placeholder {{
                color: {BB_AZUL_ESCURO} !important;
                -webkit-text-fill-color: {BB_AZUL_ESCURO} !important;
                opacity: 0.65;
            }}

            /* Widgets Streamlit/BaseWeb que podem herdar tema claro/escuro */
            div.stApp .main [data-testid="stWidgetLabel"] *,
            div.stApp .main [data-testid="stMarkdownContainer"] *,
            div.stApp .main [data-testid="stTextInputRootElement"] *,
            div.stApp .main [data-testid="stSelectbox"] *,
            div.stApp .main [data-baseweb="input"] *,
            div.stApp .main [data-baseweb="select"] * {{
                color: {BB_AZUL_ESCURO} !important;
                -webkit-text-fill-color: {BB_AZUL_ESCURO} !important;
            }}

            /* BLINDAGEM DA SIDEBAR (EXCECAO) */
            [data-testid='stSidebar'] {{
                background-color: {BB_AZUL} !important;
            }}

            [data-testid='stSidebar'] * {{
                color: {BB_BRANCO} !important;
                -webkit-text-fill-color: {BB_BRANCO} !important;
            }}

            [data-testid='stSidebar'] svg {{
                fill: {BB_BRANCO} !important;
            }}

            .bb-section-title {{
                font-size: 1.2rem;
                font-weight: 800;
                letter-spacing: -0.01em;
                margin: 1.2rem 0 0.6rem 0;
                color: {BB_AZUL_ESCURO} !important;
                -webkit-text-fill-color: {BB_AZUL_ESCURO} !important;
            }}

            /* Cards */
            .metric-card {{
                background: {BB_BRANCO} !important;
                border-radius: 16px !important;
                padding: 1.5rem !important;
                border: 1px solid #E2E8F0 !important;
                box-shadow: 0 10px 25px rgba(0, 51, 160, 0.05) !important;
                text-align: center !important;
            }}
            
            .metric-card div, .metric-card span {{
                color: {BB_AZUL_ESCURO} !important;
                -webkit-text-fill-color: {BB_AZUL_ESCURO} !important;
            }}

            /* Forca especifica nos titulos internos dos cards */
            .metric-card .card-title,
            .metric-card h1,
            .metric-card h2,
            .metric-card h3,
            .metric-card h4,
            .metric-card p,
            .metric-card label,
            .metric-card small {{
                color: {BB_AZUL_ESCURO} !important;
                -webkit-text-fill-color: {BB_AZUL_ESCURO} !important;
            }}

            .status-card {{
                background: {BB_BRANCO} !important;
                border-radius: 16px !important;
                padding: 1rem 1.25rem !important;
                border-left: 4px solid {BB_AZUL} !important;
                box-shadow: 0 8px 20px rgba(0, 51, 160, 0.05) !important;
            }}

            /* Botões em estilo pílula */
            div.stButton > button {{
                background-color: {BB_AMARELO} !important;
                color: {BB_AZUL_ESCURO} !important;
                -webkit-text-fill-color: {BB_AZUL_ESCURO} !important;
                border: none !important;
                border-radius: 50px !important;
                font-weight: 800 !important;
                padding: 0.6rem 2.5rem !important;
                box-shadow: 0 4px 12px rgba(255, 204, 0, 0.3) !important;
            }}

            div.stButton > button:focus,
            .stTextInput > div > div > input:focus,
            .stSelectbox > div > div:focus-within {{
                outline: 3px solid rgba(0, 51, 160, 0.25) !important;
                outline-offset: 2px !important;
            }}

            /* Inputs da aba Ajustes */
            .stTextInput input,
            .stSelectbox div[data-baseweb="select"],
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea,
            .stSelectbox > div > div,
            .stSelectbox > div > div > div,
            .stSelectbox option,
            [data-testid="stFileUploaderDropzone"] {{
                background: {BB_BRANCO} !important;
                background-color: {BB_BRANCO} !important;
                color: {BB_AZUL_ESCURO} !important;
                -webkit-text-fill-color: {BB_AZUL_ESCURO} !important;
                border: 1px solid #D7DFEA !important;
                border-radius: 12px !important;
            }}

            .stSelectbox div[data-baseweb="select"] * {{
                color: {BB_AZUL_ESCURO} !important;
                -webkit-text-fill-color: {BB_AZUL_ESCURO} !important;
            }}

            /* Mantem o header visivel para preservar o controle de recolher/expandir sidebar */
            #MainMenu, footer {{ visibility: hidden; }}

            header {{
                visibility: visible !important;
                display: block !important;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

# 4. Componentes de UI
def render_header(title, subtitle):
    st.markdown(f'<h1 style="color:{BB_AZUL_ESCURO}; margin-bottom:0;">{title}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:{BB_AZUL_ESCURO}; margin-top:0; font-weight:500;">{subtitle}</p>', unsafe_allow_html=True)


def render_section_title(title):
    st.markdown(f"<div class='bb-section-title'>{title}</div>", unsafe_allow_html=True)


def render_status(message):
    st.markdown(f"<div class='status-card'>{message}</div>", unsafe_allow_html=True)

def render_metrics():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="card-title" style="font-size:0.8rem; font-weight:700; opacity:0.7;">SCORE DE SAUDE</div><div style="font-size:1.8rem; font-weight:800; color:{BB_AZUL_ESCURO} !important;">{st.session_state.score}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="card-title" style="font-size:0.8rem; font-weight:700; opacity:0.7;">ENDIVIDAMENTO</div><div style="font-size:1.8rem; font-weight:800; color:{BB_AZUL_ESCURO} !important;">{int(st.session_state.taxa_endividamento*100)}%</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="card-title" style="font-size:0.8rem; font-weight:700; opacity:0.7;">ROI PREVISTO</div><div style="font-size:1.8rem; font-weight:800; color:{BB_AZUL_ESCURO} !important;">R$ {st.session_state.roi:,.0f}</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="card-title" style="font-size:0.8rem; font-weight:700; opacity:0.7;">FLUXO DE CAIXA</div><div style="font-size:1.8rem; font-weight:800; color:{BB_AZUL_ESCURO} !important;">R$ {st.session_state.fluxo_caixa:,.0f}</div></div>', unsafe_allow_html=True)

# 5. Execução Principal
def main():
    st.set_page_config(
        page_title='Banco do Brasil | Dashboard Financeiro',
        page_icon='https://www.bb.com.br/favicon.ico',
        layout='wide',
        initial_sidebar_state='expanded'
    )

    # CSS com prioridade maxima: primeira chamada de renderizacao apos set_page_config.
    apply_styles()
    init_session_state()

    # Sidebar
    st.sidebar.markdown("<h2 style='font-weight:800; letter-spacing:-1px;'>BANCO DO BRASIL</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    aba = st.sidebar.radio("MENU PRINCIPAL", ["Dashboard", "Documentos", "IA", "Ajustes"])

    if aba == "Dashboard":
        render_header("Futuro das Minhas Finanças", "Olá, João Silva | Open Finance BB")
        render_metrics()
        render_section_title("Historico de Gastos Mensais")
        df = pd.DataFrame({"Categoria": ["Moradia", "Alimentação", "Lazer", "Saúde"], "Valor": [1800, 950, 620, 430]})
        fig = px.bar(df, x="Categoria", y="Valor", color_discrete_sequence=[BB_AZUL])
        fig.update_layout(
            template="plotly_white",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=BB_AZUL_ESCURO),
            title_font=dict(color=BB_AZUL_ESCURO),
            legend=dict(font=dict(color=BB_AZUL_ESCURO)),
            hoverlabel=dict(font=dict(color=BB_AZUL_ESCURO), bgcolor=BB_BRANCO)
        )
        fig.update_xaxes(
            title_font=dict(color=BB_AZUL_ESCURO),
            tickfont=dict(color=BB_AZUL_ESCURO),
            color=BB_AZUL_ESCURO
        )
        fig.update_yaxes(
            title_font=dict(color=BB_AZUL_ESCURO),
            tickfont=dict(color=BB_AZUL_ESCURO),
            color=BB_AZUL_ESCURO
        )
        st.plotly_chart(fig, use_container_width=True)

    elif aba == "Documentos":
        render_header("Gestão de Documentos", "Envie suas Cédulas de Crédito para análise inteligente")
        st.markdown("<div class='metric-card' style='text-align:left;'>", unsafe_allow_html=True)
        arquivo = st.file_uploader("Upload de Documento (PDF/JPG/PNG)", type=["pdf", "jpg", "png"])
        if arquivo:
            render_status(f"Arquivo {arquivo.name} recebido. Pronto para analise.")
        st.markdown("</div>", unsafe_allow_html=True)

    elif aba == "IA":
        render_header("Insights de IA", "Análise preditiva baseada no seu perfil")
        if not st.session_state.analisado:
            render_status("Aguardando processamento de documentos para gerar insights personalizados.")
        else:
            render_status("Insight: Seu potencial de investimento aumentou R$ 700,00 este mes.")

    else:
        render_header("Ajustes de Perfil", "Personalize sua experiência no Open Finance")
        st.markdown("<div class='metric-card' style='text-align:left;'>", unsafe_allow_html=True)
        st.text_input("Nome Completo", value="João Silva")
        st.selectbox("Perfil de Investidor", ["Conservador", "Moderado", "Arrojado"])
        st.button("Salvar Preferências")
        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()