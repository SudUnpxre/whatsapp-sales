from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Configurações do Ambiente
    PROJECT_NAME: str = "WhatsApp Sales Automation"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here"  # openssl rand -hex 32
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"

    # Configurações do Banco de Dados
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: Optional[str] = None
    
    # Configurações do Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Configurações do Mercado Pago
    MERCADO_PAGO_ACCESS_TOKEN: Optional[str] = None
    MERCADO_PAGO_PUBLIC_KEY: Optional[str] = None
    
    # Configurações do OpenAI
    OPENAI_API_KEY: Optional[str] = None

    # Configurações do WhatsApp
    WHATSAPP_ACCESS_TOKEN: Optional[str] = None
    WHATSAPP_PHONE_NUMBER_ID: Optional[str] = None
    WHATSAPP_BUSINESS_ID: Optional[str] = None
    WHATSAPP_VERIFY_TOKEN: Optional[str] = None

    class Config:
        case_sensitive = True
        env_file = ".env"

    def __init__(self, **data):
        super().__init__(**data)
        
        if not self.DATABASE_URL and self.POSTGRES_DB:
            self.DATABASE_URL = (
                f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
            )

settings = Settings() 