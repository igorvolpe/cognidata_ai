# ⚡ CogniData AI — Enterprise Intelligence Copilot & Unstructured Lakehouse

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red.svg)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/Database-SQLite_Lakehouse-green.svg)](https://www.sqlite.org/)
[![Architecture](https://img.shields.io/badge/Architecture-ETL_%2B_RAG_%2B_Text--to--SQL-purple.svg)](#-arquitetura-da-solução)

> **CogniData AI** é uma plataforma de inteligência de dados de ponta a ponta que transforma documentos não-estruturados (contratos em PDF/TXT e transcrições de áudio/atendimento) em um **Data Lakehouse Relacional indexado**, munido de um **Agente Cognitivo Autônomo** para análise de risco de churn, auditoria contratual e inteligência de negócios em tempo real.

---

## 📐 Arquitetura da Solução

```mermaid
flowchart TD
    subgraph RawData ["1. Dados Não-Estruturados (Raw)"]
        A[Contratos Jurídicos .txt]
        B[Transcrições de Suporte .txt]
    end

    subgraph Pipeline ["2. Engine de ETL & Structuring"]
        C[Regex Extractors & Parsers]
        D[Normalizador de Entidades & KPIs]
    end

    subgraph Lakehouse ["3. Structured Lakehouse"]
        E[(tb_contratos)]
        F[(tb_atendimentos)]
    end

    subgraph CopilotEngine ["4. Agente Cognitivo (CogniData Engine)"]
        G[Intent Classifier & Intent Routing]
        H[Text-to-SQL Compiler]
        I[Document Search RAG Engine]
    end

    subgraph Frontend ["5. Interface Executiva (Streamlit)"]
        J[Copilot Chat Interface]
        K[Data Explorer & Export CSV]
        L[Auditoria de Contratos Brutos]
    end

    A --> C
    B --> C
    C --> D
    D --> E
    D --> F
    E --> H
    F --> H
    A --> I
    B --> I
    G --> H
    G --> I
    H --> J
    I --> J
    E --> K
    F --> K
    A --> L
    B --> L

    🔥 Funcionalidades ChaveParsing Automático de Textos Desestruturados: Algoritmos em Python e Regex avançado extraem entidades complexas como CNPJ, Vigência, Multa Revisional, Ticket Mensal e Churn Risk Score de documentos brutos.Data Lakehouse Relacional (SQLite): Schema analítico otimizado (tb_contratos e tb_atendimentos) projetado para consultas SQL agregadas de alta performance.Agente Cognitivo Hybrid (Text-to-SQL + RAG):Text-to-SQL: Converte perguntas em linguagem natural em queries SQL complexas (com GROUP BY, JOIN, e ordenação de risco).Document RAG: Varre o conteúdo textual bruto para localizar cláusulas jurídicas específicas (ex: rescisão, multa e suspensão).Painel Web Interativo (Streamlit Enterprise):Copilot Chat: Assistente conversacional com atalhos de análise rápida.Data Lake Explorer: Inspeção de dados com download instantâneo de relatórios em formato CSV.Auditor de Documentos: Leitor integrado de contratos e transcrições em tempo real.🛠️ Tecnologias UtilizadasCamadaTecnologiaAplicaçãoLinguagem CorePython 3.10+Processamento de dados, lógica do agente e pipelinesPipeline ETLRe (Regex) / OSExtração de padrão em lote e parsing de textoLakehouse AnalyticsSQLite3 / PandasArmazenamento relacional e manipulação tabularAgente CognitivoCustom RAG + Text-to-SQLRoteamento de intenção e geração SQL sintéticaUser InterfaceStreamlitFrontend interativo, visualização e exportação🚀 Como Executar o ProjetoPré-requisitosTer o Python 3.10 ou superior instalado na sua máquina.1️⃣ Clonar o RepositórioBashgit clone [https://github.com/seu-usuario/cognidata_ai.git](https://github.com/seu-usuario/cognidata_ai.git)
cd cognidata_ai
2️⃣ Instalar as DependênciasBashpip install streamlit pandas
3️⃣ Processar os Dados Brutos e Construir o LakehouseExecute o orquestrador do pipeline. Ele irá gerar os documentos sintéticos em data/raw/ e compilar o banco relacional em data/processed/cognidata.db:Bashpython build_lakehouse.py
4️⃣ Iniciar a Aplicação CopilotBashpython -m streamlit run app.py
Acesse no seu navegador em: http://localhost:8501📊 Estrutura do Banco de Dados (Lakehouse)📌 tb_contratoscliente (TEXT) — Nome da empresa contratanteservico (TEXT) — Tipo de solução/software contratadovalor_mensal (REAL) — Recorrência mensal (MRR)vigencia_meses (INTEGER) — Duração total em mesesvalor_total_contrato (REAL) — Total do contrato (ARR/LTV)multa_percentual (REAL) — % de rescisão antecipadarisco_financeiro (TEXT) — Classificação (Baixo, Médio, Alto)📌 tb_atendimentoscliente (TEXT) — Identificação da empresagravidade (TEXT) — Nível do chamadoclassificacao (TEXT) — Sentimento detectado na conversachurn_risk_score (INTEGER) — Nota de 0 a 10 para probabilidade de cancelamento📝 LicençaEste projeto está sob a licença MIT. Sinta-se à vontade para utilizar, modificar e contribuir!Developed with ⚡ by Igor