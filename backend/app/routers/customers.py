from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.core import deps
from app.database import get_db
from app.crud.crud_customer import customer as crud_customer
from app.crud.crud_order import order as crud_order
from app.schemas.customer import Customer, CustomerCreate, CustomerUpdate
from app.schemas.order import Order
from app.schemas.auth import User
from app.services.whatsapp_service import whatsapp_service

router = APIRouter()

@router.get("/", response_model=List[Customer])
async def get_customers(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Retorna a lista de clientes.
    """
    customers = crud_customer.get_multi(db, skip=skip, limit=limit)
    return customers

@router.post("/", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def create_customer(
    *,
    db: Session = Depends(get_db),
    customer_in: CustomerCreate,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Cria um novo cliente.
    """
    # Verifica se já existe cliente com este número
    customer = crud_customer.get_by_whatsapp(
        db, whatsapp_number=customer_in.whatsapp_number
    )
    if customer:
        raise HTTPException(
            status_code=400,
            detail="Cliente com este número de WhatsApp já existe"
        )
    
    customer = crud_customer.create(db, obj_in=customer_in)
    return customer

@router.get("/{customer_id}", response_model=Customer)
async def get_customer(
    *,
    db: Session = Depends(get_db),
    customer_id: int,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Retorna um cliente específico pelo ID.
    """
    customer = crud_customer.get(db, id=customer_id)
    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )
    return customer

@router.put("/{customer_id}", response_model=Customer)
async def update_customer(
    *,
    db: Session = Depends(get_db),
    customer_id: int,
    customer_in: CustomerUpdate,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Atualiza um cliente.
    """
    customer = crud_customer.get(db, id=customer_id)
    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )
    customer = crud_customer.update(db, db_obj=customer, obj_in=customer_in)
    return customer

@router.get("/{customer_id}/orders", response_model=List[Order])
async def get_customer_orders(
    *,
    db: Session = Depends(get_db),
    customer_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Retorna os pedidos de um cliente específico.
    """
    customer = crud_customer.get(db, id=customer_id)
    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )
    return customer.orders[skip : skip + limit]

@router.post("/{customer_id}/send-message")
async def send_message(
    *,
    db: Session = Depends(get_db),
    customer_id: int,
    message: Dict[str, Any],
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Envia uma mensagem para um cliente via WhatsApp.
    """
    customer = crud_customer.get(db, id=customer_id)
    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )
    
    try:
        # Envia mensagem via WhatsApp
        response = await whatsapp_service.send_message(
            phone_number=customer.whatsapp_number,
            message=message["content"]
        )
        
        # Registra a interação
        crud_customer.update_interaction(
            db,
            db_obj=customer,
            interaction_data={
                "type": "message_sent",
                "content": message["content"],
                "status": "success"
            }
        )
        
        return {"status": "success", "message_id": response.get("message_id")}
    
    except Exception as e:
        # Registra a falha na interação
        crud_customer.update_interaction(
            db,
            db_obj=customer,
            interaction_data={
                "type": "message_sent",
                "content": message["content"],
                "status": "error",
                "error": str(e)
            }
        )
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao enviar mensagem: {str(e)}"
        )

@router.get("/active", response_model=List[Customer])
async def get_active_customers(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Retorna a lista de clientes ativos (que interagiram nos últimos 30 dias).
    """
    customers = crud_customer.get_active_customers(db, skip=skip, limit=limit)
    return customers 