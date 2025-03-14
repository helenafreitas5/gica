import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import time

# Carregando variáveis de ambiente
load_dotenv()

# Configurando a página
st.set_page_config(
    page_title="The Ultimate Storyselling Agency Checklist",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado para uma aparência futurista
st.markdown("""
<style>
    /* Cores e fontes principais */
    :root {
        --primary-color: #7B2CBF;
        --secondary-color: #9D4EDD;
        --accent-color: #C77DFF;
        --text-color: #E0AAFF;
        --dark-bg: #10002B;
        --card-bg: #240046;
        --glow: 0 0 10px rgba(201, 122, 255, 0.5);
    }
    
    /* Estilo geral da página */
    .main {
        background: linear-gradient(135deg, var(--dark-bg) 0%, #1A0040 100%);
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Cabeçalho */
    h1, h2, h3 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    
    /* Containers */
    .css-18e3th9, .css-1d391kg {
        padding: 1rem 2rem;
    }
    
    /* Cartões de mensagem */
    .chat-container {
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: var(--glow);
        background: var(--card-bg);
        border-left: 4px solid var(--accent-color);
        transition: all 0.3s ease;
    }
    
    .chat-container:hover {
        box-shadow: 0 0 20px rgba(201, 122, 255, 0.8);
        transform: translateY(-2px);
    }
    
    .user-msg {
        border-left: 4px solid var(--primary-color);
        background: rgba(36, 0, 70, 0.7);
    }
    
    .assistant-msg {
        border-left: 4px solid var(--accent-color);
    }
    
    /* Botões e inputs */
    .stButton>button {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 25px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: var(--glow);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 15px rgba(201, 122, 255, 0.8);
    }
    
    .stTextInput>div>div>input {
        background: rgba(36, 0, 70, 0.3);
        border: 1px solid var(--accent-color);
        border-radius: 10px;
        color: white;
        padding: 15px;
    }
    
    /* Elementos decorativos */
    .decorative-line {
        height: 4px;
        background: linear-gradient(90deg, var(--primary-color), transparent);
        margin: 10px 0 30px 0;
        border-radius: 2px;
    }
    
    /* Animação de digitação */
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    
    .typing-effect {
        overflow: hidden;
        white-space: nowrap;
        animation: typing 3.5s steps(40, end);
    }
    
    /* Animação de pulso para ícones */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .pulse-icon {
        animation: pulse 2s infinite;
        display: inline-block;
        margin-right: 10px;
    }
    
    /* Loading spinner personalizado */
    .loading-spinner {
        text-align: center;
        margin: 20px 0;
    }
    
    .spinner-dot {
        display: inline-block;
        width: 12px;
        height: 12px;
        margin: 0 5px;
        background-color: var(--accent-color);
        border-radius: 50%;
        animation: spinner-pulse 1.4s infinite ease-in-out;
    }
    
    .spinner-dot:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .spinner-dot:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes spinner-pulse {
        0%, 80%, 100% { 
            transform: scale(0);
            opacity: 0.5;
        }
        40% { 
            transform: scale(1);
            opacity: 1;
        }
    }
</style>
""", unsafe_allow_html=True)

# Inicializar o estado da sessão
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = os.getenv('OPENAI_API_KEY', '')

if 'openai_assistant_id' not in st.session_state:
    st.session_state.openai_assistant_id = os.getenv('OPENAI_ASSISTANT_ID', '')

# Sidebar para configurações
with st.sidebar:
    st.title("⚙️ Configurações")
    
    with st.expander("🔑 API Keys"):
        openai_api_key = st.text_input(
            "OpenAI API Key",
            value=st.session_state.openai_api_key,
            type="password",
            help="Insira sua chave API da OpenAI"
        )
        
        openai_assistant_id = st.text_input(
            "Assistant ID",
            value=st.session_state.openai_assistant_id,
            help="ID do assistente da OpenAI"
        )
        
        if st.button("Salvar configurações"):
            st.session_state.openai_api_key = openai_api_key
            st.session_state.openai_assistant_id = openai_assistant_id
            st.success("Configurações salvas com sucesso!")

    st.markdown("---")
    
    st.markdown("""
    ### Sobre o Storyselling Checklist
    
    O Storyselling Checklist é uma metodologia desenvolvida por Gica Trierweiler para criar histórias de vendas poderosas para sua agência.
    
    Este assistente irá te ajudar a criar e aprimorar o storytelling da sua agência seguindo esta metodologia.
    """)

# Cabeçalho principal
col1, col2 = st.columns([3, 1])
with col1:
    st.title("✨ The Ultimate Storyselling Agency Checklist")
    st.markdown("<p class='typing-effect'>Te ajudo a gabaritar o Storyselling Checklist de Gica Trierweiler!</p>", unsafe_allow_html=True)

with col2:
    st.image("https://api.placeholders.dev/image?size=150x150&text=✨&textColor=%23ffffff&backgroundColor=%237B2CBF", width=150)

# Linha decorativa
st.markdown("<div class='decorative-line'></div>", unsafe_allow_html=True)

# Função para processar a mensagem usando a API da OpenAI
def process_message(user_input):
    if not st.session_state.openai_api_key:
        st.error("Por favor, configure sua API Key da OpenAI na sidebar.")
        return "Erro: API Key não configurada."
    
    if not st.session_state.openai_assistant_id:
        st.error("Por favor, configure o ID do Assistente da OpenAI na sidebar.")
        return "Erro: ID do Assistente não configurado."
    
    try:
        client = OpenAI(api_key=st.session_state.openai_api_key)
        
        # Criar um thread
        thread = client.beta.threads.create()
        
        # Adicionar mensagem ao thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )
        
        # Executar o assistente
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=st.session_state.openai_assistant_id
        )
        
        # Aguardar a conclusão
        while run.status in ["queued", "in_progress"]:
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
        
        # Obter as mensagens
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        
        # Retornar a resposta mais recente do assistente
        for message in messages.data:
            if message.role == "assistant":
                content = message.content[0].text.value
                return content
        
        return "Não foi possível obter uma resposta do assistente."
    
    except Exception as e:
        st.error(f"Erro ao processar a mensagem: {str(e)}")
        return f"Erro: {str(e)}"

# Exibir mensagens anteriores
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f"<div class='chat-container user-msg'><b>Você:</b><br>{message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-container assistant-msg'><b>Assistente:</b><br>{message['content']}</div>", unsafe_allow_html=True)

# Input do usuário
with st.container():
    user_input = st.text_area("O que você gostaria de saber sobre o Storyselling Checklist?", height=100)
    
    col1, col2 = st.columns([6, 1])
    with col1:
        send_button = st.button("Enviar mensagem ✉️")
    with col2:
        clear_button = st.button("Limpar 🗑️")

# Processamento da mensagem
if send_button and user_input:
    # Adicionar mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Mostrar loading
    with st.container():
        st.markdown("<div class='loading-spinner'><div class='spinner-dot'></div><div class='spinner-dot'></div><div class='spinner-dot'></div></div>", unsafe_allow_html=True)
    
    # Processar a mensagem
    response = process_message(user_input)
    
    # Adicionar resposta ao histórico
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Recarregar a página para mostrar a nova mensagem
    st.experimental_rerun()

# Limpar histórico
if clear_button:
    st.session_state.messages = []
    st.experimental_rerun()

# Rodapé
st.markdown("---")
st.markdown("<center>© 2025 The Ultimate Storyselling Agency Checklist | Powered by OpenAI</center>", unsafe_allow_html=True)
