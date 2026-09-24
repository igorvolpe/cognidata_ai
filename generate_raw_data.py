import os
import random

# Criar diretórios de saída
os.makedirs("data/raw/contracts", exist_ok=True)
os.makedirs("data/raw/transcripts", exist_ok=True)

CLIENTES = [
    "TechCorp Brasil", "Varejo Mais", "Logistica Express", "Indústrias Alfa",
    "BioSaúde Soluções", "Nexus Tecnologia", "Global Trade LTDA", "Inovação Digital"
]

ESTADOS = ["SP", "RJ", "MG", "SC", "PR", "BA"]
SERVICOS = ["Suporte Cloud 24/7", "Licenciamento SaaS Enterprise", "Consultoria em Segurança", "Desenvolvimento Sob Medida"]

# --- 1. GERAÇÃO DE CONTRATOS (DOCUMENTO TEXTO NATIVO) ---
def generate_contracts(num_contracts=20):
    print(f"📄 Gerando {num_contracts} contratos de clientes...")
    for i in range(1, num_contracts + 1):
        cliente = random.choice(CLIENTES)
        estado = random.choice(ESTADOS)
        servico = random.choice(SERVICOS)
        valor_mensal = round(random.uniform(5000, 45000), 2)
        multa_percentual = random.choice([10, 15, 20, 25])
        vigencia_meses = random.choice([12, 24, 36])
        data_inicio = f"2024-0{random.randint(1,9)}-15"
        
        text = f"""CONTRATO DE PRESTAÇÃO DE SERVIÇOS TÉCNICOS

CONTRATANTE: {cliente}, localizado em {estado}.
CONTRATADA: CogniData Services S.A.

CLÁUSULA PRIMEIRA - DO OBJETO:
O presente contrato tem como objeto a prestação de serviços de {servico} para a CONTRATANTE.

CLÁUSULA SEGUNDA - DOS VALORES E CONDIÇÕES:
Pela prestação dos serviços, a CONTRATANTE pagará o valor mensal de R$ {valor_mensal:,.2f}.
O prazo de vigência deste instrumento é de {vigencia_meses} meses, com início em {data_inicio}.

CLÁUSULA TERCEIRA - DA RESCISÃO E MULTA:
A rescisão antecipada por qualquer das partes sem justa causa implicará multa rescisória de {multa_percentual}% sobre o valor restante do contrato.
Em caso de atraso no pagamento por mais de 30 dias, haverá suspensão imediata do serviço.

CLÁUSULA QUARTA - DO FORO:
Fica eleito o foro da comarca de São Paulo/SP para dirimir quaisquer dúvidas decorrentes deste contrato.

São Paulo, {data_inicio}.
__________________________________________
CogniData Services & {cliente}
"""
        file_path = f"data/raw/contracts/contrato_{i:03d}_{cliente.replace(' ', '_')}.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)

# --- 2. GERAÇÃO DE TRANSCRIÇÕES DE ATENDIMENTO ---
def generate_transcripts(num_transcripts=15):
    print(f"🎙️ Gerando {num_transcripts} transcrições de atendimento...")
    
    PROBLEMAS = [
        ("Indisponibilidade do sistema no horário de pico", "Alta", "Insatisfeito / Churn Risk"),
        ("Dúvida simples sobre emissão de fatura", "Baixa", "Neutro"),
        ("Lentidão ao carregar relatórios executivos", "Média", "Insatisfeito"),
        ("Solicitação de upgrade de plano empresarial", "Baixa", "Satisfeito / Expansão"),
        ("Instabilidade recorrente na API de integração", "Alta", "Insatisfeito / Churn Risk")
    ]
    
    for i in range(1, num_transcripts + 1):
        cliente = random.choice(CLIENTES)
        problema, gravidade, sentimento = random.choice(PROBLEMAS)
        atendente = random.choice(["Carlos Silva", "Mariana Costa", "Roberto Alves", "Juliana Lima"])
        
        content = f"""TRANSCRIÇÃO DE CHAMADA DE SUPORTE #SUP-{i:04d}
Data: 2024-08-{random.randint(10,28)}
Cliente: {cliente}
Atendente: {atendente}
Gravidade: {gravidade}
Classificação Preliminar: {sentimento}

[Atendente]: Olá, aqui é o {atendente} do suporte CogniData. Como posso ajudar a {cliente} hoje?
[Cliente]: Olá. Estamos enfrentando problemas sérios com {problema.lower()}. Isso está impactando nossa operação!
[Atendente]: Entendo perfeitamente a gravidade. Deixe-me verificar o status dos servidores e abrir um chamado de prioridade {gravidade}.
[Cliente]: Preciso de uma solução urgente. Se isso continuar, teremos que rever nosso contrato e avaliar o cancelamento.
[Atendente]: Compreendo sua frustração. Já encaminhei para a equipe de Engenharia Nível 3. O protocolo do atendimento é #PROT-{random.randint(10000,99999)}.
"""
        file_path = f"data/raw/transcripts/transcricao_{i:03d}_{cliente.replace(' ', '_')}.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

if __name__ == "__main__":
    generate_contracts(20)
    generate_transcripts(15)
    print("✅ Massa de dados não-estruturada gerada com sucesso em data/raw/!")