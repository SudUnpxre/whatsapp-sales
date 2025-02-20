from typing import Optional
from pydantic_settings import BaseSettings

class ProductionSettings(BaseSettings):
    # Configurações do Ambiente
    PROJECT_NAME: str = "WhatsApp Sales Automation"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"

    # Configurações do Banco de Dados
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    # Configurações do Redis
    REDIS_URL: str

    # Configurações do Mercado Pago
    MERCADO_PAGO_ACCESS_TOKEN: str
    MERCADO_PAGO_PUBLIC_KEY: str

    # Configurações do OpenAI
    OPENAI_API_KEY: str

    # Configurações do WhatsApp
    WHATSAPP_API_TOKEN: str
    WHATSAPP_PHONE_NUMBER_ID: str
    WHATSAPP_BUSINESS_ID: str
    WHATSAPP_VERIFY_TOKEN: str

    # Configurações de Segurança
    ALLOWED_HOSTS: list[str] = ["*"]
    CORS_ORIGINS: list[str] = ["*"]
    SSL_KEYFILE: Optional[str] = None
    SSL_CERTFILE: Optional[str] = None

    # Configurações de Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    class Config:
        case_sensitive = True
        env_file = ".env.prod"

    def __init__(self, **data):
        super().__init__(**data)

        if not self.SQLALCHEMY_DATABASE_URI and self.POSTGRES_DB:
            self.SQLALCHEMY_DATABASE_URI = (
                f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
            )

settings = ProductionSettings() 