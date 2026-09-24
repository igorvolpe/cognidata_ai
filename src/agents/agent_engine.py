import sqlite3
import os

DB_PATH = "data/processed/cognidata.db"

class CogniDataAgent:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def _execute_query(self, query):
        """Executa comandos SQL no Lakehouse e retorna resultados estruturados."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            conn.close()
            return columns, rows
        except Exception as e:
            conn.close()
            return None, str(e)

    def search_documents(self, keyword):
        """Busca textual avançada em contratos e transcrições."""
        matches = []
        folders = ["data/raw/contracts", "data/raw/transcripts"]
        
        for folder in folders:
            if not os.path.exists(folder):
                continue
            for file in os.listdir(folder):
                if file.endswith(".txt"):
                    path = os.path.join(folder, file)
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if keyword.lower() in content.lower():
                            matches.append((file, folder.split('/')[-1], content))
        return matches

    def ask(self, user_prompt):
        """Motor RAG e Text-to-SQL do Agente Cognitivo."""
        prompt_lower = user_prompt.lower()
        
        # --- INTENÇÃO 1: Análise de Risco / Churn Agrupada por Cliente ---
        if any(w in prompt_lower for w in ["churn", "risco", "cancelar", "cancelamento", "insatisfeito"]):
            sql = """
            SELECT 
                a.cliente, 
                MAX(a.gravidade) as gravidade, 
                MAX(a.classificacao) as sentimento, 
                MAX(a.churn_risk_score) as max_score, 
                COALESCE(SUM(DISTINCT c.valor_total_contrato), 0) as valor_total_contratos,
                COALESCE(MAX(c.multa_percentual), 0) as multa_max
            FROM tb_atendimentos a
            LEFT JOIN tb_contratos c ON a.cliente = c.cliente
            WHERE a.churn_risk_score >= 6
            GROUP BY a.cliente
            ORDER BY max_score DESC, valor_total_contratos DESC
            """
            cols, rows = self._execute_query(sql)
            if not rows:
                return "🤖 **Agente CogniData:** Não identifiquei clientes com alto risco de churn no momento."
            
            response = "🤖 **Agente CogniData - Relatório Consolidado de Risco & Churn:**\n\n"
            response += "| Cliente | Gravidade Máx. | Sentimento | Score Risco | Recorrência Total | Multa Média |\n"
            response += "|---|---|---|---|---|---|\n"
            for r in rows:
                valor = f"R$ {r[4]:,.2f}"
                multa = f"{r[5]}%"
                response += f"| **{r[0]}** | {r[1]} | {r[2]} | {r[3]}/10 | {valor} | {multa} |\n"
            
            response += "\n💡 **Insight Estratégico:** Os dados foram consolidados por cliente para evitar sobreposição. Priorize contato direto com os clientes com Score ≥ 8."
            return response

        # --- INTENÇÃO 2: Maiores Contratos / Financeiro ---
        elif any(w in prompt_lower for w in ["maiores contratos", "faturamento", "receita", "valor total", "financeiro"]):
            sql = """
            SELECT cliente, estado, servico, valor_mensal, vigencia_meses, valor_total_contrato, risco_financeiro
            FROM tb_contratos
            ORDER BY valor_total_contrato DESC
            LIMIT 5
            """
            cols, rows = self._execute_query(sql)
            
            response = "🤖 **Agente CogniData - Top 5 Maiores Contratos da Carteira:**\n\n"
            response += "| Cliente | UF | Serviço | Mensalidade | Vigência | Total Contratado | Classif. Risco |\n"
            response += "|---|---|---|---|---|---|---|\n"
            for r in rows:
                response += f"| **{r[0]}** | {r[1]} | {r[2]} | R$ {r[3]:,.2f} | {r[4]} meses | R$ {r[5]:,.2f} | {r[6]} |\n"
            return response

        # --- INTENÇÃO 3: Distribuição Geográfica ---
        elif any(w in prompt_lower for w in ["serviço", "servico", "estado", "uf", "distribuição", "resumo"]):
            sql = """
            SELECT estado, COUNT(*) as qtd_contratos, SUM(valor_total_contrato) as faturamento_total
            FROM tb_contratos
            GROUP BY estado
            ORDER BY faturamento_total DESC
            """
            cols, rows = self._execute_query(sql)
            
            response = "🤖 **Agente CogniData - Distribuição Geográfica de Faturamento:**\n\n"
            response += "| Estado (UF) | Qtd Contratos | Faturamento Total |\n"
            response += "|---|---|---|\n"
            for r in rows:
                response += f"| **{r[0]}** | {r[1]} | R$ {r[2]:,.2f} |\n"
            return response

        # --- INTENÇÃO 4: Pesquisa de Cláusulas Contratuais / Termos ---
        elif any(w in prompt_lower for w in ["cláusula", "clausula", "multa", "suspensão", "foro"]):
            matches = self.search_documents("cláusula")
            if not matches:
                matches = self.search_documents("multa")
                
            response = "🤖 **Agente CogniData - Análise de Cláusulas Contratuais Encontradas:**\n\n"
            for doc, folder, text in matches[:3]:
                response += f"📄 **Arquivo:** `{doc}`\n"
                lines = [line.strip() for line in text.split("\n") if "CLÁUSULA" in line or "MULTA" in line]
                for l in lines[:2]:
                    response += f"> _{l}_\n"
                response += "\n---\n"
            return response

        # --- INTENÇÃO 5: Fallback Busca Textual ---
        else:
            words = [w for w in prompt_lower.split() if len(w) > 3]
            matches = []
            for w in words:
                found = self.search_documents(w)
                matches.extend(found)
            
            if matches:
                matches_uniq = list(set([(m[0], m[1]) for m in matches]))
                response = f"🤖 **Agente CogniData - Documentos Relacionados Encontrados:**\n\n"
                for doc, folder in matches_uniq[:5]:
                    response += f"• 📄 **[{folder.upper()}]** `{doc}`\n"
                return response
            else:
                return "🤖 **Agente CogniData:** Como posso ajudar? Tente perguntar sobre:\n- *'Análise de risco de churn'* \n- *'Quais os maiores contratos?'*\n- *'Cláusulas de multa nos contratos'* \n- *'Faturamento por estado'*"