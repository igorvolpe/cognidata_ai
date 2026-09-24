# ⚡ CogniData AI — Enterprise Intelligence Copilot

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![SQLite](https://img.shields.io/badge/SQLite-Lakehouse-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

Plataforma de inteligência de dados que transforma documentos não-estruturados (contratos jurídicos e transcrições de atendimento) em um **Data Lakehouse Relacional**, integrando um **Agente Cognitivo Autônomo (Text-to-SQL + RAG)** para auditoria contratual e prevenção de churn.

---

## 🎯 Arquitetura da Solução

```mermaid
flowchart TD
    subgraph Inputs ["1. Fontes de Dados Não-Estruturados"]
        A[📄 Contratos Jurídicos .txt]
        B[💬 Transcrições de Atendimento .txt]
    end

    subgraph ETL ["2. Pipeline de Processamento (ETL)"]
        C[🔍 Extração com Regex & Rules]
        D[🧹 Normalizador & Estruturador]
    end

    subgraph Lakehouse ["3. Data Lakehouse (SQLite)"]
        E[(📊 tb_contratos)]
        F[(📊 tb_atendimentos)]
    end

    subgraph Agent ["4. Agente Cognitivo Autônomo"]
        G[🎯 Roteador de Intenções]
        H[💻 Engine Text-to-SQL]
        I[📑 RAG - Busca Documental]
    end

    subgraph UI ["5. Dashboard Executivo (Streamlit)"]
        J[💬 Chat Copilot]
        K[📈 Explorer do Data Lakehouse]
    end

    A --> C
    B --> C
    C --> D
    D --> E
    D --> F

    G --> H
    G --> I

    E --> H
    F --> H
    A --> I
    B --> I

    H --> J
    I --> J
    E --> K
    F --> K

🔥 Principais Recursos:
- ETL não-estruturado: Extração automática de CNPJ, vigência, multa revisional, MRR e risco de churn via Regex e regras de negócio.
- Data Lakehouse Analítico: Armazenamento relacional e otimizado em SQLite (tb_contratos e tb_atendimentos).
- Agente Cognitivo Híbrido: Engine Text-to-SQL: Converte perguntas em linguagem natural diretamente em consultas relacionais agregadas. Document RAG: Busca semântica e profunda de cláusulas contratuais e termos jurídicos nos arquivos originais.
- Interface Interativa: Painel construído em Streamlit com chat em tempo real, navegação por abas e exportação de relatórios em CSV.

🛠️ Tecnologias Utilizadas
- Camada: Linguagem Base, Parsing & Regex, Data Lakehouse, Interface Web.
- Tecnologia: Python 3.10+, re (Standard Library), SQLite3 / Pandas, Streamlit.
- Função no Projeto: Lógica de processamento, agentes e pipeline. Extração de entidades e padrões textuais. Armazenamento analítico e manipulação de tabelas. Frontend interativo, visualização de dados e chat

📂 Estrutura do Repositório
cognidata_ai/
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

🚀 Como Executar o Projeto
1. Clonar o Repositório
Bash
git clone [https://github.com/igorvolpe/cognidata_ai.git](https://github.com/igorvolpe/cognidata_ai.git)
cd cognidata_ai
2. Instalar as Dependências
Bash
pip install -r requirements.txt
3. Processar Dados e Gerar o Lakehouse
Bash
python build_lakehouse.py
4. Iniciar a Aplicação Streamlit
Bash
python -m streamlit run app.py
Acesse o painel no navegador através do endereço http://localhost:8501

📄 Licença
Este projeto está sob a licença MIT. Desenvolvido por Igor Volpe.

---

### 📤 Atualizar no GitHub (Passo Final)

Depois de salvar o arquivo no VS Code, rode estes 3 comandos rápidos no terminal para atualizar o seu GitHub:

```powershell
git add README.md
git commit -m "docs: atualização completa do README com diagramas e layout profissional"
git push
