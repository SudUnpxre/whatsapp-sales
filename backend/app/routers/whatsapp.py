from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.core import deps
from app.database import get_db
from app.crud.crud_customer import customer as crud_customer
from app.crud.crud_product import product as crud_product
from app.services.whatsapp_service import whatsapp_service
from app.services.ai_service import ai_service
from app.schemas.auth import User

router = APIRouter()

@router.post("/webhook")
async def whatsapp_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Webhook para receber mensagens do WhatsApp.
    """
    try:
        data = await request.json()
        
        # Verificar se é uma mensagem de entrada
        if "entry" in data and len(data["entry"]) > 0:
            for entry in data["entry"]:
                if "changes" in entry and len(entry["changes"]) > 0:
                    for change in entry["changes"]:
                        if change["value"].get("messages"):
                            for message in change["value"]["messages"]:
                                # Processar a mensagem
                                await process_incoming_message(db, message)
        
        return {"status": "success"}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar webhook: {str(e)}"
        )

async def process_incoming_message(db: Session, message: Dict[str, Any]):
    """
    Processa uma mensagem recebida do WhatsApp.
    """
    try:
        # Extrair informações da mensagem
        whatsapp_number = message["from"]
        message_text = message.get("text", {}).get("body", "")
        
        # Buscar ou criar cliente
        customer, created = crud_customer.get_or_create(
            db,
            whatsapp_number=whatsapp_number,
            defaults={"name": "Cliente WhatsApp"}
        )
        
        # Registrar interação
        crud_customer.update_interaction(
            db,
            db_obj=customer,
            interaction_data={
                "type": "message_received",
                "content": message_text,
                "message_id": message["id"]
            }
        )
        
        # Processar mensagem com IA
        ai_response = await ai_service.process_message_with_ai(message_text)
        
        if ai_response["should_respond"]:
            # Enviar resposta
            response = await whatsapp_service.send_message(
                phone_number=whatsapp_number,
                message=ai_response["response"]
            )
            
            # Registrar resposta
            crud_customer.update_interaction(
                db,
                db_obj=customer,
                interaction_data={
                    "type": "message_sent",
                    "content": ai_response["response"],
                    "message_id": response.get("message_id")
                }
            )
            
            # Se a IA identificou intenção de compra, enviar catálogo
            if ai_response.get("intent") == "purchase_intent":
                products = crud_product.get_active(db, skip=0, limit=5)
                product_list = "\n".join([
                    f"• {p.name}: R$ {p.price:.2f}"
                    for p in products
                ])
                catalog_message = (
                    "Aqui estão alguns dos nossos produtos:\n\n"
                    f"{product_list}\n\n"
                    "Gostaria de mais informações sobre algum deles?"
                )
                
                await whatsapp_service.send_message(
                    phone_number=whatsapp_number,
                    message=catalog_message
                )
    
    except Exception as e:
        print(f"Erro ao processar mensagem: {str(e)}")

@router.post("/send-message")
async def send_message(
    *,
    db: Session = Depends(get_db),
    message_data: Dict[str, Any],
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Envia uma mensagem via WhatsApp.
    """
    try:
        response = await whatsapp_service.send_message(
            phone_number=message_data["phone_number"],
            message=message_data["content"]
        )
        
        # Buscar cliente
        customer = crud_customer.get_by_whatsapp(
            db,
            whatsapp_number=message_data["phone_number"]
        )
        
        if customer:
            # Registrar interação
            crud_customer.update_interaction(
                db,
                db_obj=customer,
                interaction_data={
                    "type": "message_sent",
                    "content": message_data["content"],
                    "message_id": response.get("message_id"),
                    "sent_by": current_user.email
                }
            )
        
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao enviar mensagem: {str(e)}"
        )

@router.post("/send-template")
async def send_template(
    *,
    db: Session = Depends(get_db),
    template_data: Dict[str, Any],
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Envia uma mensagem de template via WhatsApp.
    """
    try:
        response = await whatsapp_service.send_template(
            phone_number=template_data["phone_number"],
            template_name=template_data["template_name"],
            language_code=template_data.get("language_code", "pt_BR"),
            components=template_data.get("components")
        )
        
        # Buscar cliente
        customer = crud_customer.get_by_whatsapp(
            db,
            whatsapp_number=template_data["phone_number"]
        )
        
        if customer:
            # Registrar interação
            crud_customer.update_interaction(
                db,
                db_obj=customer,
                interaction_data={
                    "type": "template_sent",
                    "template_name": template_data["template_name"],
                    "message_id": response.get("message_id"),
                    "sent_by": current_user.email
                }
            )
        
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao enviar template: {str(e)}"
        )

@router.get("/templates")
async def get_templates(
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Lista os templates disponíveis.
    """
    try:
        templates = await whatsapp_service.get_templates()
        return templates
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar templates: {str(e)}"
        ) 