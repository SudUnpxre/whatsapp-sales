import mercadopago
from typing import Dict, Any, Optional
from app.core.config import settings

class PaymentService:
    def __init__(self):
        self.sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
    
    async def create_payment(
        self,
        payment_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Cria um pagamento no Mercado Pago.
        """
        try:
            # Preparar os dados do pagamento
            preference_data = {
                "items": [
                    {
                        "title": item["product_name"],
                        "quantity": item["quantity"],
                        "unit_price": item["unit_price"],
                        "currency_id": "BRL"
                    }
                    for item in payment_data["items"]
                ],
                "payer": {
                    "email": payment_data["customer_email"],
                    "name": payment_data["customer_name"]
                },
                "external_reference": str(payment_data["id"]),
                "back_urls": {
                    "success": f"{settings.API_V1_STR}/payments/success",
                    "failure": f"{settings.API_V1_STR}/payments/failure",
                    "pending": f"{settings.API_V1_STR}/payments/pending"
                },
                "auto_return": "approved",
                "notification_url": f"{settings.API_V1_STR}/payments/webhook"
            }
            
            # Criar a preferência
            preference_response = self.sdk.preference().create(preference_data)
            preference = preference_response["response"]
            
            return {
                "payment_id": preference["id"],
                "init_point": preference["init_point"],
                "sandbox_init_point": preference["sandbox_init_point"]
            }
        
        except Exception as e:
            print(f"Erro ao criar pagamento: {str(e)}")
            raise
    
    async def check_payment_status(
        self,
        payment_id: str
    ) -> Dict[str, Any]:
        """
        Verifica o status de um pagamento.
        """
        try:
            payment = self.sdk.payment().get(payment_id)
            return {
                "status": payment["response"]["status"],
                "status_detail": payment["response"]["status_detail"],
                "payment_method": payment["response"]["payment_method"]
            }
        
        except Exception as e:
            print(f"Erro ao verificar status do pagamento: {str(e)}")
            raise
    
    async def refund_payment(
        self,
        payment_id: str,
        refund_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Processa o reembolso de um pagamento.
        """
        try:
            # Se não houver dados específicos de reembolso, reembolsar o valor total
            if not refund_data:
                refund = self.sdk.refund().create(payment_id)
            else:
                refund = self.sdk.refund().create(payment_id, refund_data)
            
            return {
                "refund_id": refund["response"]["id"],
                "status": refund["response"]["status"]
            }
        
        except Exception as e:
            print(f"Erro ao processar reembolso: {str(e)}")
            raise
    
    async def process_webhook(
        self,
        webhook_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Processa webhooks do Mercado Pago.
        """
        try:
            if webhook_data["type"] == "payment":
                payment_info = self.sdk.payment().get(webhook_data["data"]["id"])
                return {
                    "type": "payment",
                    "id": payment_info["response"]["id"],
                    "status": payment_info["response"]["status"],
                    "external_reference": payment_info["response"]["external_reference"],
                    "transaction_amount": payment_info["response"]["transaction_amount"],
                    "payment_method": payment_info["response"]["payment_method"]
                }
            
            return {"type": webhook_data["type"], "processed": True}
        
        except Exception as e:
            print(f"Erro ao processar webhook: {str(e)}")
            raise
    
    async def get_payment_methods(self) -> Dict[str, Any]:
        """
        Retorna os métodos de pagamento disponíveis.
        """
        try:
            payment_methods = self.sdk.payment_methods().list()
            return payment_methods["response"]
        
        except Exception as e:
            print(f"Erro ao obter métodos de pagamento: {str(e)}")
            raise

payment_service = PaymentService() 