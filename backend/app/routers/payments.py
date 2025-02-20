from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.core import deps
from app.database import get_db
from app.crud.crud_order import order as crud_order
from app.services.payment_service import payment_service
from app.schemas.auth import User

router = APIRouter()

@router.post("/create")
async def create_payment(
    *,
    db: Session = Depends(get_db),
    order_id: int,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Cria um pagamento para um pedido.
    """
    # Buscar o pedido
    order = crud_order.get_by_id_and_user(
        db=db, id=order_id, user_id=current_user.id
    )
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )
    
    # Verificar se o pedido já tem pagamento
    if order.payment_id:
        raise HTTPException(
            status_code=400,
            detail="Este pedido já possui um pagamento"
        )
    
    try:
        # Preparar dados do pagamento
        payment_data = {
            "id": order.id,
            "total_amount": order.total_amount,
            "items": [
                {
                    "product_name": item.product.name,
                    "quantity": item.quantity,
                    "unit_price": item.price
                }
                for item in order.items
            ],
            "customer_email": current_user.email,
            "customer_name": current_user.full_name
        }
        
        # Criar pagamento
        payment = await payment_service.create_payment(payment_data)
        
        # Atualizar pedido com ID do pagamento
        order = crud_order.update_status(
            db=db,
            db_obj=order,
            status="pending",
            payment_id=payment["payment_id"]
        )
        
        return payment
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao criar pagamento: {str(e)}"
        )

@router.get("/status/{payment_id}")
async def check_payment_status(
    payment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Verifica o status de um pagamento.
    """
    # Buscar o pedido pelo payment_id
    order = crud_order.get_by_payment_id(db=db, payment_id=payment_id)
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Pagamento não encontrado"
        )
    
    # Verificar se o pedido pertence ao usuário
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Acesso negado"
        )
    
    try:
        payment_status = await payment_service.check_payment_status(payment_id)
        return payment_status
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao verificar status do pagamento: {str(e)}"
        )

@router.post("/webhook")
async def payment_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Webhook para receber notificações de pagamento do Mercado Pago.
    """
    try:
        data = await request.json()
        webhook_response = await payment_service.process_webhook(data)
        
        if webhook_response["type"] == "payment":
            # Buscar o pedido
            order = crud_order.get_by_payment_id(
                db=db,
                payment_id=webhook_response["id"]
            )
            
            if order:
                # Atualizar status do pedido
                new_status = webhook_response["status"]
                if new_status == "approved":
                    order_status = "paid"
                elif new_status in ["cancelled", "refunded"]:
                    order_status = "cancelled"
                else:
                    order_status = "pending"
                
                crud_order.update_status(
                    db=db,
                    db_obj=order,
                    status=order_status
                )
        
        return {"status": "success"}
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao processar webhook: {str(e)}"
        )

@router.get("/methods")
async def get_payment_methods(
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Lista os métodos de pagamento disponíveis.
    """
    try:
        payment_methods = await payment_service.get_payment_methods()
        return payment_methods
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao listar métodos de pagamento: {str(e)}"
        )

@router.post("/success")
async def payment_success(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Endpoint para redirecionamento após pagamento bem-sucedido.
    """
    try:
        # Extrair parâmetros da query
        params = dict(request.query_params)
        payment_id = params.get("payment_id")
        
        if payment_id:
            # Buscar o pedido
            order = crud_order.get_by_payment_id(db=db, payment_id=payment_id)
            if order:
                # Atualizar status do pedido
                crud_order.update_status(
                    db=db,
                    db_obj=order,
                    status="paid"
                )
        
        return {"status": "success", "message": "Pagamento processado com sucesso"}
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao processar retorno do pagamento: {str(e)}"
        )

@router.post("/failure")
async def payment_failure(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Endpoint para redirecionamento após falha no pagamento.
    """
    try:
        # Extrair parâmetros da query
        params = dict(request.query_params)
        payment_id = params.get("payment_id")
        
        if payment_id:
            # Buscar o pedido
            order = crud_order.get_by_payment_id(db=db, payment_id=payment_id)
            if order:
                # Atualizar status do pedido
                crud_order.update_status(
                    db=db,
                    db_obj=order,
                    status="pending"
                )
        
        return {"status": "failure", "message": "Falha no processamento do pagamento"}
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao processar retorno do pagamento: {str(e)}"
        ) 