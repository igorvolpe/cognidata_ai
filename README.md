# ⚡ CogniData AI — Enterprise Intelligence Copilot

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![SQLite](https://img.shields.io/badge/SQLite-Lakehouse-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

Plataforma de inteligência de dados que transforma documentos não-estruturados (contratos jurídicos e transcrições de atendimento) em um **Data Lakehouse Relacional**, integrando um **Agente Cognitivo Autônomo (Text-to-SQL + RAG)** para auditoria contratual e prevenção de churn.

---

## 🎯 Arquitetura da Solução

```mermaid
graph TD
    A[Contratos Juridicos .txt] --> C[ETL e Extracao Regex]
    B[Transcricoes Atendimento .txt] --> C
    
    C --> D[Data Lakehouse SQLite]
    
    D --> E[Agente Text-to-SQL]
    A --> F[Document RAG]
    B --> F
    
    E --> G[Dashboard Streamlit]
    F --> G
🔥 Principais RecursosETL não-estruturado: Extração automática de CNPJ, vigência, multa revisional, MRR e risco de churn via Regex e regras de negócio.Data Lakehouse Analítico: Armazenamento relacional e otimizado em SQLite (tb_contratos e tb_atendimentos).Agente Cognitivo Híbrido:Engine Text-to-SQL: Converte perguntas em linguagem natural diretamente em consultas relacionais agregadas.Document RAG: Busca semântica e profunda de cláusulas contratuais e termos jurídicos nos arquivos originais.Interface Interativa: Painel construído em Streamlit com chat em tempo real, navegação por abas e exportação de relatórios em CSV.🛠️ Tecnologias UtilizadasCamadaTecnologiaFunção no ProjetoLinguagem BasePython 3.10+Lógica de processamento, agentes e pipelineParsing & Regexre (Standard Library)Extração de entidades e padrões textuaisData LakehouseSQLite3 / PandasArmazenamento analítico e manipulação de tabelasInterface WebStreamlitFrontend interativo, visualização de dados e chat📂 Estrutura do RepositórioPlaintextcognidata_ai/
├── data/
│   ├── raw/                 # Documentos brutos (Contratos e Transcrições)
│   └── processed/           # Banco de dados SQLite gerado (cognidata.db)
├── src/
│   ├── agents/              # Módulo do Agente Cognitivo (agent_engine.py)
│   └── data_pipeline/       # Scripts de geração e ETL dos dados
├── app.py                   # Aplicação Principal (Streamlit)
├── build_lakehouse.py       # Script orquestrador da carga do Lakehouse
├── requirements.txt         # Lista de dependências Python
└── README.md                # Documentação oficial do repositório
🚀 Como Executar o Projeto1. Clonar o RepositórioBashgit clone https://github.com/igorvolpe/cognidata_ai.git
cd cognidata_ai
2. Instalar as DependênciasBashpip install -r requirements.txt
3. Processar Dados e Gerar o LakehouseBashpython build_lakehouse.py
4. Iniciar a Aplicação StreamlitBashpython -m streamlit run app.py
Acesse o painel no navegador através do endereço http://localhost:8501.📄 LicençaEste projeto está sob a licença MIT. Desenvolvido por Igor Volpe.
