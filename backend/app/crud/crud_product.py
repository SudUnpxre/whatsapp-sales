from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Product
from app.schemas.product import ProductCreate, ProductUpdate

class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        return (
            db.query(self.model)
            .filter(Product.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_owner(
        self, db: Session, *, obj_in: ProductCreate, owner_id: int
    ) -> Product:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_active(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        return (
            db.query(self.model)
            .filter(Product.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id_and_owner(
        self, db: Session, *, id: int, owner_id: int
    ) -> Optional[Product]:
        return (
            db.query(self.model)
            .filter(Product.id == id, Product.owner_id == owner_id)
            .first()
        )

product = CRUDProduct(Product) 