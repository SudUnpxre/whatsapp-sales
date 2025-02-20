from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate

class CRUDCustomer(CRUDBase[Customer, CustomerCreate, CustomerUpdate]):
    def get_by_whatsapp(
        self, db: Session, *, whatsapp_number: str
    ) -> Optional[Customer]:
        return (
            db.query(self.model)
            .filter(Customer.whatsapp_number == whatsapp_number)
            .first()
        )

    def get_by_email(
        self, db: Session, *, email: str
    ) -> Optional[Customer]:
        return (
            db.query(self.model)
            .filter(Customer.email == email)
            .first()
        )

    def get_active_customers(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Customer]:
        """Retorna clientes que interagiram nos últimos 30 dias"""
        thirty_days_ago = datetime.utcnow() - datetime.timedelta(days=30)
        return (
            db.query(self.model)
            .filter(Customer.last_interaction >= thirty_days_ago)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_interaction(
        self,
        db: Session,
        *,
        db_obj: Customer,
        interaction_data: Dict[str, Any]
    ) -> Customer:
        # Atualiza o histórico de interações
        if not db_obj.interaction_history:
            db_obj.interaction_history = []
        
        # Adiciona timestamp à interação
        interaction_data["timestamp"] = datetime.utcnow().isoformat()
        db_obj.interaction_history.append(interaction_data)
        
        # Atualiza última interação
        db_obj.last_interaction = datetime.utcnow()
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_or_create(
        self,
        db: Session,
        *,
        whatsapp_number: str,
        defaults: Dict[str, Any]
    ) -> tuple[Customer, bool]:
        """
        Busca um cliente pelo número do WhatsApp ou cria um novo se não existir.
        Retorna uma tupla (customer, created) onde created é um booleano.
        """
        customer = self.get_by_whatsapp(db, whatsapp_number=whatsapp_number)
        if customer:
            return customer, False
        
        customer_in = CustomerCreate(
            whatsapp_number=whatsapp_number,
            **defaults
        )
        customer = self.create(db, obj_in=customer_in)
        return customer, True

customer = CRUDCustomer(Customer) 