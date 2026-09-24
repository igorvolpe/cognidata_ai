import streamlit as st
import sqlite3
import pandas as pd
import os
import sys

# Incluir src no PATH
sys.path.append(os.path.abspath("."))
from src.agents.agent_engine import CogniDataAgent

st.set_page_config(
    page_title="CogniData Copilot Enterprise",
    page_icon="⚡",
    layout="wide"
)

DB_PATH = "data/processed/cognidata.db"

@st.cache_resource
def load_agent():
    return CogniDataAgent(DB_PATH)

agent = load_agent()

# --- HEADER PRINCIPAL ---
st.title("⚡ CogniData AI — Enterprise Intelligence Copilot")
st.caption("Plataforma Integrada de IA para Auditoria Contratual, Prevenção de Churn e Lakehouse Analytics.")

# --- METRICAS NA SIDEBAR ---
st.sidebar.header("📈 Dashboard do Lakehouse")

def get_kpis():
    if not os.path.exists(DB_PATH):
        return 0, 0, 0
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*), SUM(valor_total_contrato) FROM tb_contratos")
    contratos_row = cursor.fetchone()
    total_contratos = contratos_row[0] or 0
    faturamento_total = contratos_row[1] or 0
    
    cursor.execute("SELECT COUNT(DISTINCT cliente) FROM tb_atendimentos WHERE churn_risk_score >= 8")
    churn_row = cursor.fetchone()
    alto_risco = churn_row[0] or 0
    
    conn.close()
    return total_contratos, faturamento_total, alto_risco

tot_contratos, fat_total, em_risco = get_kpis()

st.sidebar.metric("Contratos Ativos", f"{tot_contratos}")
st.sidebar.metric("Receita Total Gerenciada", f"R$ {fat_total:,.2f}")
st.sidebar.metric("Clientes em Risco Crítico", f"{em_risco}", delta="-Atenção" if em_risco > 0 else "Estável", delta_color="inverse")

st.sidebar.divider()
st.sidebar.write("### 💬 Atalhos de Análise")
if st.sidebar.button("🚨 Clientes em Risco de Churn"):
    st.session_state["user_query"] = "Quais clientes têm risco de churn?"

if st.sidebar.button("🏆 Top 5 Maiores Contratos"):
    st.session_state["user_query"] = "Quais os maiores contratos?"

if st.sidebar.button("📜 Cláusulas e Multas"):
    st.session_state["user_query"] = "Analisar cláusulas de multa"

if st.sidebar.button("📍 Faturamento por Estado"):
    st.session_state["user_query"] = "Qual a distribuição por estado?"

# --- ESTRUTURA DE ABAS NA INTERFACE ---
tab1, tab2, tab3 = st.tabs(["🤖 Copilot IA Chat", "🗄️ Lakehouse Data Explorer", "📄 Documentos Brutos"])

# --- ABA 1: CHAT INTERATIVO COM O AGENTE ---
with tab1:
    st.subheader("Conversa com o Agente Cognitivo")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Olá! Sou o **CogniData Agent**. Posso analisar seus contratos, identificar riscos operacionais e prever churn em tempo real. O que deseja consultar?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    prompt = st.chat_input("Digite sua dúvida sobre contratos, clientes ou suporte...")

    if "user_query" in st.session_state and st.session_state["user_query"]:
        prompt = st.session_state.pop("user_query")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        with st.spinner("Consultando Lakehouse e executando análise..."):
            response = agent.ask(prompt)
            
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

# --- ABA 2: EXPLORADOR DE BANCO DE DADOS (LAKEHOUSE) ---
with tab2:
    st.subheader("Visualização dos Dados Estruturados (SQLite Lakehouse)")
    
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        
        st.write("#### 📑 Tabela de Contratos Extraídos (`tb_contratos`)")
        df_contratos = pd.read_sql_query("SELECT * FROM tb_contratos", conn)
        st.dataframe(df_contratos, use_container_width=True)
        
        # Download do CSV de Contratos
        csv_contratos = df_contratos.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Exportar Contratos (CSV)", csv_contratos, "contratos_cognidata.csv", "text/csv")
        
        st.divider()
        
        st.write("#### 🎧 Tabela de Atendimentos (`tb_atendimentos`)")
        df_atendimentos = pd.read_sql_query("SELECT * FROM tb_atendimentos", conn)
        st.dataframe(df_atendimentos, use_container_width=True)
        
        # Download do CSV de Atendimentos
        csv_atendimentos = df_atendimentos.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Exportar Atendimentos (CSV)", csv_atendimentos, "atendimentos_cognidata.csv", "text/csv")
        
        conn.close()
    else:
        st.warning("Banco de dados ainda não gerado. Execute o `build_lakehouse.py` primeiro.")

# --- ABA 3: AUDITORIA DE DOCUMENTOS BRUTOS ---
with tab3:
    st.subheader("Inspeção de Documentos Brutos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 📄 Contratos em Texto (`data/raw/contracts`)")
        c_folder = "data/raw/contracts"
        if os.path.exists(c_folder):
            c_files = os.listdir(c_folder)
            selected_c = st.selectbox("Selecione um contrato para auditar:", c_files)
            if selected_c:
                with open(os.path.join(c_folder, selected_c), "r", encoding="utf-8") as f:
                    st.code(f.read(), language="text")

    with col2:
        st.write("### 🎙️ Transcrições de Atendimento (`data/raw/transcripts`)")
        t_folder = "data/raw/transcripts"
        if os.path.exists(t_folder):
            t_files = os.listdir(t_folder)
            selected_t = st.selectbox("Selecione uma transcrição para auditar:", t_files)
            if selected_t:
                with open(os.path.join(t_folder, selected_t), "r", encoding="utf-8") as f:
                    st.code(f.read(), language="text")