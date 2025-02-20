from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core import deps
from app.database import get_db
from app.crud.crud_product import product as crud_product
from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.schemas.auth import User

router = APIRouter()

@router.get("/", response_model=List[Product])
async def get_products(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Retorna a lista de produtos do usuário atual.
    """
    products = crud_product.get_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return products

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    *,
    db: Session = Depends(get_db),
    product_in: ProductCreate,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Cria um novo produto.
    """
    product = crud_product.create_with_owner(
        db=db, obj_in=product_in, owner_id=current_user.id
    )
    return product

@router.get("/{product_id}", response_model=Product)
async def get_product(
    *,
    db: Session = Depends(get_db),
    product_id: int,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Retorna um produto específico pelo ID.
    """
    product = crud_product.get_by_id_and_owner(
        db=db, id=product_id, owner_id=current_user.id
    )
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )
    return product

@router.put("/{product_id}", response_model=Product)
async def update_product(
    *,
    db: Session = Depends(get_db),
    product_id: int,
    product_in: ProductUpdate,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Atualiza um produto.
    """
    product = crud_product.get_by_id_and_owner(
        db=db, id=product_id, owner_id=current_user.id
    )
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )
    product = crud_product.update(db=db, db_obj=product, obj_in=product_in)
    return product

@router.delete("/{product_id}", response_model=Product)
async def delete_product(
    *,
    db: Session = Depends(get_db),
    product_id: int,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Remove um produto.
    """
    product = crud_product.get_by_id_and_owner(
        db=db, id=product_id, owner_id=current_user.id
    )
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )
    product = crud_product.remove(db=db, id=product_id)
    return product

@router.get("/public/active", response_model=List[Product])
async def get_active_products(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retorna a lista de produtos ativos (endpoint público).
    """
    products = crud_product.get_active(db=db, skip=skip, limit=limit)
    return products 