import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# --- Configurações da Página ---
st.set_page_config(
    page_title="Temperature",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS Personalizado para o Tema Escuro e Estilos ---
st.markdown(
    """
    <style>
    /* Estilos Gerais */
    body {
        font-family: 'Segoe UI', sans-serif;
    }

    /* Fundo principal do dashboard */
    .stApp {
        background-color: #1a1a2e; /* Azul marinho escuro */
        color: #e0e0e0; /* Texto claro */
    }

    /* Barra superior onde fica o botão Deploy */
    header[data-testid="stHeader"] {
        background-color: #1a1a2e;  /* Mesma cor do fundo */
        color: #e0e0e0;
        border-bottom: 1px solid #2c2c54;
    }

    /* Oculta botão de deploy */
    header [data-testid="stDeployButton"] {
        display: none;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1f1f3a; /* Mesmo fundo do app */
        color: #e0e0e0;
        padding: 2rem 1rem;
    }
    .stSidebar .st-emotion-cache-1j7q093 { /* Container interno da sidebar para padding */
        padding-top: 2rem;
    }
    .stSidebar .st-emotion-cache-17l4a3h { /* Título principal da sidebar */
        font-size: 1.5rem;
        font-weight: bold;
        color: #e0e0e0;
        margin-bottom: 1.5rem;
    }

    /* Estilo para os botões de navegação da sidebar */
    .stSidebar button {
        background-color: transparent !important; /* Torna o fundo transparente */
        color: #e0e0e0 !important; /* Cor do texto padrão */
        border: none !important; /* Remove a borda padrão */
        border-radius: 5px !important;
        padding: 0.5rem 1rem !important;
        margin-bottom: 0.5rem !important;
        width: 100% !important; /* Ocupa a largura total */
        text-align: left !important; /* Alinha o texto à esquerda */
        transition: background-color 0.3s !important;
    }
    .stSidebar button:hover {
        background-color: #4a4a8a !important; /* Cor ao passar o mouse */
    }
    /* Estilo para o botão de navegação ativo */
    .stSidebar button.active {
        background-color: #6a1b9a !important; /* Cor de destaque para o item ativo */
        font-weight: bold !important;
    }

    /* Títulos e Subtítulos */
    h1, h2, h3, h4, h5, h6 {
        color: #e0e0e0;
    }

    /* Cards/Seções de Conteúdo (Containers principais) */
    .st-emotion-cache-ocqkz7, .st-emotion-cache-1r6dmc7, .st-emotion-cache-1f871t6 {
        background-color: #1f1f3a; /* Fundo dos cards */
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .st-emotion-cache-1j7q093 { /* Padding para as colunas do topo */
        padding: 0 0 0 0;
    }

    /* Botões de Ação (Geral) */
    .stButton>button {
        background-color: #6a1b9a; /* Roxo vibrante */
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #8e24aa; /* Roxo mais claro ao passar o mouse */
    }

    /* Botões de ação (Edit, Delete, Info) - Específico para lista de conteúdo */
    .content-item-right button {
        background-color: #4a4a8a !important; /* Azul escuro para botões de ação */
        color: #e0e0e0 !important;
        border: 1px solid #6a6ad6 !important;
        padding: 0.3rem 0.8rem !important;
        font-size: 0.85rem !important;
        margin-left: 0.5rem !important;
        border-radius: 5px !important;
    }
    .content-item-right button:hover {
        background-color: #6a6ad6 !important;
    }

    /* Barras de Progresso */
    .stProgress>div>div>div>div {
        background-color: #6a1b9a;
    }
    .stProgress>div>div>div {
        background-color: #4a4a8a;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background: transparent;
        border-bottom: 2px solid transparent;
        border-radius: 0px;
        font-size: 1.1rem;
        color: #9e9e9e;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #e0e0e0;
    }
    .stTabs [aria-selected="true"] {
        border-bottom: 2px solid #6a1b9a !important;
        color: #e0e0e0 !important;
        font-weight: bold;
    }

    /* Cards de Conteúdo (individual na lista) */
    .content-item {
        background-color: #3e3e70;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .content-item-left {
        flex-grow: 1;
    }
    .content-item-right {
        display: flex;
        gap: 0.5rem;
    }
    .content-item h4 {
        margin-top: 0;
        margin-bottom: 0.5rem;
        color: #e0e0e0;
    }

    /* Estilo para métricas pequenas */
    
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: bold;
        color: #e0e0e0;
    }

    .st-emotion-cache-1r6dmc7 .st-emotion-cache-1t33g95 {
        background-color: #3e3e70;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    /* Estilos para inputs na página de configurações */
    .stTextInput label, .stCheckbox label, .stRadio label {
        color: #e0e0e0 !important;
    }
    .stTextInput input, .stFileUploader > div > div > button {
        background-color: #3e3e70 !important;
        color: #e0e0e0 !important;
        border: 1px solid #4a4a8a !important;
        border-radius: 5px !important;
    }
    .stFileUploader button { /* Ajusta o botão de upload de arquivo */
        background-color: #6a1b9a !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Dados de Exemplo ---
dados_temp = {
    'Mês': ['8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19'],
    'Valor': [25, 30, 32, 36, 40, 46, 47, 50, 49, 51, 55, 60]
}

df_temp = pd.DataFrame(dados_temp)

dados_categorias = {
    'Categoria': ['Cat A', 'Cat B', 'Cat C', 'Cat D', 'Cat E'],
    'Quantidade': [45, 60, 30, 70, 25]
}
df_categorias = pd.DataFrame(dados_categorias)

progresso_total = {'Temp': 70, 'Faltante': 30}
porcentagem_concluida = progresso_total['Faltante']

# --- Funções para as "Páginas" ---

def mostrar_dashboard_principal():
    st.title("Análise de Dados")

    # Seção de Métricas (topo)
    st.markdown("### Visão Geral")
    col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)

    with col_metric1:
        st.metric(label="Temperatura Mínima", value=25)
    with col_metric2:
        st.metric(label="Temperatura Máxima", value=df_temp['Valor'].max())
    with col_metric3:
        st.metric(label="Temperatura Média", value=df_temp['Valor'].min())
    with col_metric4:
        st.metric(label="Tempo de Operação (H)", value="8.5")

    st.markdown("---")

    # Seção de Gráficos (3 colunas para linha, barra e circular)
    st.subheader("Gráficos")

    col_graph1, col_space, col_graph2 = st.columns(3)

    with col_graph1:
        st.markdown("#### Historico de temperatura")
        fig_linha = go.Figure(data=go.Scatter(x=df_temp['Mês'], y=df_temp['Valor'], mode='lines+markers', line=dict(color='#6a1b9a', width=3), marker=dict(size=8, color='#c85dd1')))
        fig_linha.update_layout(
            xaxis_title="Hora",
            yaxis_title="Temperatura",
            margin=dict(t=30, b=30, l=30, r=30),
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False)
        )
        st.plotly_chart(fig_linha, use_container_width=True, config={'displayModeBar': False})

    with col_graph2:
        st.markdown("#### Temperatura")
        fig_circular = go.Figure(data=[go.Pie(
            labels=list(progresso_total.keys()),
            values=list(progresso_total.values()),
            hole=.7,
            marker_colors=['#6a1b9a', '#4a4a8a'],
            textinfo='none'
        )])
        fig_circular.update_layout(
            margin=dict(t=0, b=0, l=0, r=0),
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            annotations=[dict(text=f'{porcentagem_concluida} ºC', x=0.5, y=0.5, font_size=30, showarrow=False, font_color="#e0e0e0")]
        )
        st.plotly_chart(fig_circular, use_container_width=True, config={'displayModeBar': False})

    st.markdown("---")

def mostrar_pagina_configuracoes():
    st.title("⚙️ Configurações do Aplicativo")
    st.write("Bem-vindo à página de configurações. Aqui você pode ajustar diversas opções do seu dashboard.")

    st.markdown("---")
    st.subheader("Configurações Gerais")

    # Usando st.session_state para persistir o valor do input
    if 'nome_usuario' not in st.session_state:
        st.session_state.nome_usuario = "Usuário Padrão"
    novo_nome_usuario = st.text_input("Nome do Usuário", st.session_state.nome_usuario, key="user_name_input")
    if novo_nome_usuario != st.session_state.nome_usuario:
        st.session_state.nome_usuario = novo_nome_usuario

    st.checkbox("Receber Notificações por E-mail", True, key="email_notifications_checkbox")

    if 'tema_selecionado' not in st.session_state:
        st.session_state.tema_selecionado = "Escuro"
    novo_tema = st.radio("Tema da Interface", ["Claro", "Escuro"], index=1 if st.session_state.tema_selecionado == "Escuro" else 0, key="theme_radio")
    if novo_tema != st.session_state.tema_selecionado:
        st.session_state.tema_selecionado = novo_tema
        # Poderia adicionar lógica aqui para de fato mudar o tema CSS, mas é mais complexo em tempo de execução
        st.warning("A mudança de tema requer uma reinicialização do aplicativo para ser totalmente aplicada.")

    st.markdown("---")
    st.subheader("Gerenciamento de Dados")
    uploaded_file = st.file_uploader("Fazer Upload de Novos Dados (CSV)", type=['csv'], key="data_uploader")
    if uploaded_file is not None:
        # Aqui você processaria o arquivo carregado
        st.success(f"Arquivo '{uploaded_file.name}' carregado com sucesso!")

    if st.button("Salvar Configurações", key="save_config_button"):
        st.success("Configurações salvas!")
        # Aqui você implementaria a lógica para realmente salvar as configurações
        # ex: salvar em um arquivo, banco de dados, etc.

# --- Lógica de Navegação da Página ---
# Inicializa o estado da sessão se ainda não existir
if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = 'dashboard' # Define a página inicial como 'dashboard'

# --- Barra Lateral (Sidebar) com botões para navegação ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/893/893216.png", width=50)
    st.markdown("## Menu")
    st.markdown("---")

    # Botão Home / Dashboard
    # Usamos o st.button com um HTML personalizado para que o estilo funcione,
    # e um key único para o Streamlit identificar o botão.
    # Adicionamos uma classe 'active' ao botão se for a página atual.
    home_active_class = " active" if st.session_state.pagina_atual == 'dashboard' else ""
    if st.button(f"🏠 Home", key="sidebar_home_btn", help="Voltar para o Dashboard Principal"):
        st.session_state.pagina_atual = 'dashboard'
        st.rerun() # Adicionado para garantir a atualização imediata do UI

    st.markdown("---")

    # Botão Configurações
    config_active_class = " active" if st.session_state.pagina_atual == 'configuracoes' else ""
    if st.button(f"⚙️ Configurações", key="sidebar_config_btn", help="Ajustar as configurações do aplicativo"):
        st.session_state.pagina_atual = 'configuracoes'
        st.rerun() # Adicionado para garantir a atualização imediata do UI

# --- Renderiza a página com base no estado da sessão ---
# As funções mostrar_dashboard_principal() e mostrar_pagina_configuracoes()
# serão chamadas apenas quando a pagina_atual for a correta.
if st.session_state.pagina_atual == 'dashboard':
    mostrar_dashboard_principal()
elif st.session_state.pagina_atual == 'configuracoes':
    mostrar_pagina_configuracoes()