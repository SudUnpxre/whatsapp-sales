from typing import Dict, Any
import openai
from app.core.config import settings

class AIService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        
        self.system_prompt = """
        Você é um assistente virtual de uma loja online. Seu objetivo é ajudar os clientes com:
        1. Informações sobre produtos
        2. Realização de pedidos
        3. Acompanhamento de pedidos
        4. Dúvidas gerais sobre a loja
        
        Mantenha suas respostas curtas, diretas e amigáveis.
        Identifique a intenção do usuário e responda adequadamente.
        Se identificar intenção de compra, retorne intent: purchase_intent.
        Se não souber responder algo, seja honesto e sugira falar com um atendente humano.
        """
    
    async def process_message_with_ai(
        self,
        message: str
    ) -> Dict[str, Any]:
        """
        Processa uma mensagem usando IA para gerar uma resposta apropriada.
        """
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            # Extrair a resposta
            ai_message = response.choices[0].message.content
            
            # Verificar se há intenção de compra
            purchase_keywords = [
                "comprar", "preço", "valor", "quanto custa",
                "produtos", "catálogo", "disponível"
            ]
            has_purchase_intent = any(
                keyword in message.lower()
                for keyword in purchase_keywords
            )
            
            return {
                "should_respond": True,
                "response": ai_message,
                "intent": "purchase_intent" if has_purchase_intent else "general",
                "confidence": response.choices[0].finish_reason == "stop"
            }
        
        except Exception as e:
            print(f"Erro ao processar mensagem com IA: {str(e)}")
            return {
                "should_respond": True,
                "response": "Desculpe, estou com dificuldades técnicas no momento. Por favor, tente novamente mais tarde ou fale com um de nossos atendentes.",
                "intent": "error",
                "confidence": 0
            }
    
    async def analyze_sentiment(
        self,
        message: str
    ) -> Dict[str, Any]:
        """
        Analisa o sentimento da mensagem do cliente.
        """
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Analise o sentimento da mensagem e classifique como: POSITIVO, NEGATIVO ou NEUTRO. Retorne apenas a classificação."
                    },
                    {"role": "user", "content": message}
                ],
                temperature=0,
                max_tokens=10
            )
            
            sentiment = response.choices[0].message.content.strip().upper()
            return {
                "sentiment": sentiment,
                "confidence": response.choices[0].finish_reason == "stop"
            }
        
        except Exception as e:
            print(f"Erro ao analisar sentimento: {str(e)}")
            return {
                "sentiment": "NEUTRO",
                "confidence": 0
            }
    
    async def extract_product_info(
        self,
        message: str
    ) -> Dict[str, Any]:
        """
        Extrai informações sobre produtos mencionados na mensagem.
        """
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """
                        Extraia informações sobre produtos mencionados na mensagem.
                        Retorne um JSON com:
                        - product_name: nome do produto mencionado
                        - quantity: quantidade mencionada (default: 1)
                        - specific_info: informações específicas solicitadas (preço, cor, tamanho, etc)
                        """
                    },
                    {"role": "user", "content": message}
                ],
                temperature=0,
                max_tokens=150
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"Erro ao extrair informações do produto: {str(e)}")
            return None

ai_service = AIService() 