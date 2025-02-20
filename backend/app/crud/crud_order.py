from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Order, OrderItem, Product
from app.schemas.order import OrderCreate, OrderUpdate

class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        return (
            db.query(self.model)
            .filter(Order.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_items(
        self, db: Session, *, obj_in: OrderCreate, user_id: int
    ) -> Order:
        # Criar o pedido
        order_data = obj_in.model_dump(exclude={"items"})
        db_order = Order(**order_data, user_id=user_id)
        db.add(db_order)
        db.flush()  # Obter o ID do pedido sem commit

        # Criar os itens do pedido
        for item in obj_in.items:
            db_item = OrderItem(
                order_id=db_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price
            )
            db.add(db_item)
            
            # Atualizar o estoque do produto
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product:
                product.stock -= item.quantity
                db.add(product)

        db.commit()
        db.refresh(db_order)
        return db_order

    def get_by_id_and_user(
        self, db: Session, *, id: int, user_id: int
    ) -> Optional[Order]:
        return (
            db.query(self.model)
            .filter(Order.id == id, Order.user_id == user_id)
            .first()
        )

    def get_by_payment_id(
        self, db: Session, *, payment_id: str
    ) -> Optional[Order]:
        return (
            db.query(self.model)
            .filter(Order.payment_id == payment_id)
            .first()
        )

    def update_status(
        self, db: Session, *, db_obj: Order, status: str, payment_id: Optional[str] = None
    ) -> Order:
        db_obj.status = status
        if payment_id:
            db_obj.payment_id = payment_id
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

order = CRUDOrder(Order) 