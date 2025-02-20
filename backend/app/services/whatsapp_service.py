import httpx
from typing import Dict, Any, List, Optional
from app.core.config import settings

class WhatsAppService:
    def __init__(self):
        self.base_url = "https://graph.facebook.com/v17.0"
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.access_token = settings.WHATSAPP_ACCESS_TOKEN
        self.verify_token = settings.WHATSAPP_VERIFY_TOKEN
        
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    async def send_message(
        self,
        phone_number: str,
        message: str
    ) -> Dict[str, Any]:
        """
        Envia uma mensagem de texto via WhatsApp.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/{self.phone_number_id}/messages",
                headers=self.headers,
                json={
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": phone_number,
                    "type": "text",
                    "text": {"body": message}
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def send_template(
        self,
        phone_number: str,
        template_name: str,
        language_code: str = "pt_BR",
        components: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Envia uma mensagem de template via WhatsApp.
        """
        template_data = {
            "name": template_name,
            "language": {"code": language_code}
        }
        
        if components:
            template_data["components"] = components
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/{self.phone_number_id}/messages",
                headers=self.headers,
                json={
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": phone_number,
                    "type": "template",
                    "template": template_data
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def get_templates(self) -> List[Dict[str, Any]]:
        """
        Lista os templates disponíveis.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/{settings.WHATSAPP_BUSINESS_ID}/message_templates",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json().get("data", [])
    
    async def mark_message_as_read(
        self,
        message_id: str
    ) -> Dict[str, Any]:
        """
        Marca uma mensagem como lida.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/{self.phone_number_id}/messages",
                headers=self.headers,
                json={
                    "messaging_product": "whatsapp",
                    "status": "read",
                    "message_id": message_id
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def send_location(
        self,
        phone_number: str,
        latitude: float,
        longitude: float,
        name: Optional[str] = None,
        address: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Envia uma localização via WhatsApp.
        """
        location_data = {
            "latitude": latitude,
            "longitude": longitude
        }
        
        if name:
            location_data["name"] = name
        if address:
            location_data["address"] = address
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/{self.phone_number_id}/messages",
                headers=self.headers,
                json={
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": phone_number,
                    "type": "location",
                    "location": location_data
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def send_image(
        self,
        phone_number: str,
        image_url: str,
        caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Envia uma imagem via WhatsApp.
        """
        image_data = {"link": image_url}
        if caption:
            image_data["caption"] = caption
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/{self.phone_number_id}/messages",
                headers=self.headers,
                json={
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": phone_number,
                    "type": "image",
                    "image": image_data
                }
            )
            response.raise_for_status()
            return response.json()

whatsapp_service = WhatsAppService() 