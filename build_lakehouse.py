import os
import re
import sqlite3

# Garantir diretório de saída
os.makedirs("data/processed", exist_ok=True)

DB_PATH = "data/processed/cognidata.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabela 1: Contratos Extraídos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tb_contratos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        arquivo TEXT,
        cliente TEXT,
        estado TEXT,
        servico TEXT,
        valor_mensal REAL,
        vigencia_meses INTEGER,
        valor_total_contrato REAL,
        multa_percentual REAL,
        data_inicio TEXT,
        risco_financeiro TEXT
    )
    """)
    
    # Tabela 2: Transcrições de Atendimento
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tb_atendimentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        arquivo TEXT,
        chamada_id TEXT,
        data_chamada TEXT,
        cliente TEXT,
        atendente TEXT,
        gravidade TEXT,
        classificacao TEXT,
        protocolo TEXT,
        churn_risk_score INTEGER
    )
    """)
    
    conn.commit()
    conn.close()

def parse_contracts():
    contracts_dir = "data/raw/contracts"
    if not os.path.exists(contracts_dir):
        print("❌ Diretório de contratos não encontrado.")
        return []
        
    records = []
    files = [f for f in os.listdir(contracts_dir) if f.endswith(".txt")]
    
    for file in files:
        path = os.path.join(contracts_dir, file)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Extração de Metadados via Regex
        cliente_match = re.search(r"CONTRATANTE:\s*([^,]+)", content)
        estado_match = re.search(r"localizado em\s*([A-Z]{2})", content)
        servico_match = re.search(r"prestação de serviços de\s*([^para]+)para", content)
        valor_match = re.search(r"valor mensal de R\$\s*([\d\.,]+)", content)
        vigencia_match = re.search(r"vigência deste instrumento é de\s*(\d+)\s*meses", content)
        multa_match = re.search(r"multa rescisória de\s*(\d+)%", content)
        data_match = re.search(r"início em\s*([\d]{4}-[\d]{2}-[\d]{2})", content)
        
        cliente = cliente_match.group(1).strip() if cliente_match else "Desconhecido"
        estado = estado_match.group(1).strip() if estado_match else "NA"
        servico = servico_match.group(1).strip() if servico_match else "Geral"
        
        valor_str = valor_match.group(1).replace(".", "").replace(",", ".") if valor_match else "0.0"
        valor_mensal = float(valor_str)
        
        vigencia = int(vigencia_match.group(1)) if vigencia_match else 12
        multa = float(multa_match.group(1)) if multa_match else 0.0
        data_inicio = data_match.group(1) if data_match else "2024-01-01"
        
        valor_total = round(valor_mensal * vigencia, 2)
        
        # Lógica de Risco Financeiro
        if valor_total > 500000 and multa >= 20:
            risco = "ALTO IMPACTO"
        elif valor_total > 200000:
            risco = "MÉDIO IMPACTO"
        else:
            risco = "PADRÃO"
            
        records.append((file, cliente, estado, servico, valor_mensal, vigencia, valor_total, multa, data_inicio, risco))
        
    return records

def parse_transcripts():
    transcripts_dir = "data/raw/transcripts"
    if not os.path.exists(transcripts_dir):
        print("❌ Diretório de transcrições não encontrado.")
        return []
        
    records = []
    files = [f for f in os.listdir(transcripts_dir) if f.endswith(".txt")]
    
    for file in files:
        path = os.path.join(transcripts_dir, file)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            
        chamada_match = re.search(r"#SUP-(\d+)", content)
        data_match = re.search(r"Data:\s*([\d]{4}-[\d]{2}-[\d]{2})", content)
        cliente_match = re.search(r"Cliente:\s*([^\n]+)", content)
        atendente_match = re.search(r"Atendente:\s*([^\n]+)", content)
        gravidade_match = re.search(r"Gravidade:\s*([^\n]+)", content)
        classificacao_match = re.search(r"Classificação Preliminar:\s*([^\n]+)", content)
        protocolo_match = re.search(r"#PROT-(\d+)", content)
        
        chamada_id = f"SUP-{chamada_match.group(1)}" if chamada_match else "SUP-0000"
        data_chamada = data_match.group(1) if data_match else "2024-08-01"
        cliente = cliente_match.group(1).strip() if cliente_match else "Desconhecido"
        atendente = atendente_match.group(1).strip() if atendente_match else "Sistema"
        gravidade = gravidade_match.group(1).strip() if gravidade_match else "Baixa"
        classificacao = classificacao_match.group(1).strip() if classificacao_match else "Neutro"
        protocolo = f"PROT-{protocolo_match.group(1)}" if protocolo_match else "PROT-00000"
        
        # Calcular Score de Risco de Churn (1 a 10)
        score = 2
        if "Alta" in gravidade:
            score += 4
        elif "Média" in gravidade:
            score += 2
            
        if "Insatisfeito" in classificacao or "Churn" in classificacao:
            score += 4
            
        records.append((file, chamada_id, data_chamada, cliente, atendente, gravidade, classificacao, protocolo, score))
        
    return records

def process_etl():
    print("⚡ Iniciando ETL de Dados Não-Estruturados...")
    init_db()
    
    contratos = parse_contracts()
    transcricoes = parse_transcripts()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Limpar tabelas para reprocessamento
    cursor.execute("DELETE FROM tb_contratos")
    cursor.execute("DELETE FROM tb_atendimentos")
    
    # Inserir Contratos
    cursor.executemany("""
    INSERT INTO tb_contratos (arquivo, cliente, estado, servico, valor_mensal, vigencia_meses, valor_total_contrato, multa_percentual, data_inicio, risco_financeiro)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, contratos)
    
    # Inserir Atendimentos
    cursor.executemany("""
    INSERT INTO tb_atendimentos (arquivo, chamada_id, data_chamada, cliente, atendente, gravidade, classificacao, protocolo, churn_risk_score)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, transcricoes)
    
    conn.commit()
    conn.close()
    
    print(f"✅ ETL Concluído! {len(contratos)} contratos e {len(transcricoes)} transcrições processados e salvos em {DB_PATH}.")

if __name__ == "__main__":
    process_etl()