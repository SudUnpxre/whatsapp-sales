from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core import deps
from app.database import get_db
from app.crud.crud_order import order as crud_order
from app.schemas.order import Order, OrderCreate, OrderUpdate
from app.schemas.auth import User
from app.services.payment_service import payment_service

router = APIRouter()

@router.get("/", response_model=List[Order])
async def get_orders(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Retorna a lista de pedidos do usuário atual.
    """
    orders = crud_order.get_by_user(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return orders

@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(
    *,
    db: Session = Depends(get_db),
    order_in: OrderCreate,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Cria um novo pedido.
    """
    order = crud_order.create_with_items(
        db=db, obj_in=order_in, user_id=current_user.id
    )
    
    # Criar pagamento no Mercado Pago
    try:
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
        payment = await payment_service.create_payment(payment_data)
        
        if payment:
            # Atualizar pedido com ID do pagamento
            order = crud_order.update_status(
                db=db,
                db_obj=order,
                status="pending",
                payment_id=payment.get("payment_id")
            )
    except Exception as e:
        # Log do erro e continuar, já que o pedido foi criado
        print(f"Erro ao criar pagamento: {str(e)}")
    
    return order

@router.get("/{order_id}", response_model=Order)
async def get_order(
    *,
    db: Session = Depends(get_db),
    order_id: int,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Retorna um pedido específico pelo ID.
    """
    order = crud_order.get_by_id_and_user(
        db=db, id=order_id, user_id=current_user.id
    )
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )
    return order

@router.put("/{order_id}", response_model=Order)
async def update_order(
    *,
    db: Session = Depends(get_db),
    order_id: int,
    order_in: OrderUpdate,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Atualiza um pedido.
    """
    order = crud_order.get_by_id_and_user(
        db=db, id=order_id, user_id=current_user.id
    )
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )
    
    # Se estiver cancelando o pedido, verificar se é possível
    if order_in.status == "cancelled" and order.status not in ["pending", "paid"]:
        raise HTTPException(
            status_code=400,
            detail="Não é possível cancelar este pedido"
        )
    
    order = crud_order.update(db=db, db_obj=order, obj_in=order_in)
    return order

@router.post("/{order_id}/cancel", response_model=Order)
async def cancel_order(
    *,
    db: Session = Depends(get_db),
    order_id: int,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Cancela um pedido.
    """
    order = crud_order.get_by_id_and_user(
        db=db, id=order_id, user_id=current_user.id
    )
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )
    
    if order.status not in ["pending", "paid"]:
        raise HTTPException(
            status_code=400,
            detail="Não é possível cancelar este pedido"
        )
    
    # Se o pedido estiver pago, tentar reembolso
    if order.status == "paid" and order.payment_id:
        try:
            refund_data = {"payment_id": order.payment_id}
            await payment_service.refund_payment(order.payment_id, refund_data)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Erro ao processar reembolso: {str(e)}"
            )
    
    order = crud_order.update_status(db=db, db_obj=order, status="cancelled")
    return order

@router.get("/{order_id}/payment-status")
async def get_payment_status(
    *,
    db: Session = Depends(get_db),
    order_id: int,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Verifica o status do pagamento de um pedido.
    """
    order = crud_order.get_by_id_and_user(
        db=db, id=order_id, user_id=current_user.id
    )
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )
    
    if not order.payment_id:
        return {"status": "no_payment", "message": "Nenhum pagamento associado"}
    
    try:
        payment_status = await payment_service.check_payment_status(order.payment_id)
        return payment_status
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao verificar status do pagamento: {str(e)}"
        ) 