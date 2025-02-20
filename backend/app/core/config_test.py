from typing import Optional
from pydantic_settings import BaseSettings

class TestSettings(BaseSettings):
    # Configurações do Ambiente
    PROJECT_NAME: str = "WhatsApp Sales Automation (Test)"
    DEBUG: bool = True
    ENVIRONMENT: str = "test"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "test-secret-key-not-for-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    # Configurações do Banco de Dados
    POSTGRES_SERVER: str = "db-test"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "test_whatsapp_sales"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    # Configurações do Redis
    REDIS_URL: str = "redis://redis-test:6379/0"
    REDIS_PASSWORD: str = "redis"

    # Configurações do Mercado Pago (Sandbox)
    MERCADO_PAGO_ACCESS_TOKEN: str = "TEST-0000000000000000-000000-00000000000000000000000000000000-000000000"
    MERCADO_PAGO_PUBLIC_KEY: str = "TEST-00000000-0000-0000-0000-000000000000"

    # Configurações do OpenAI (opcional para testes)
    OPENAI_API_KEY: str = "sk-test-key"

    # Configurações do WhatsApp (mock para testes)
    WHATSAPP_API_TOKEN: str = "test-token"
    WHATSAPP_PHONE_NUMBER_ID: str = "test-phone-id"
    WHATSAPP_BUSINESS_ID: str = "test-business-id"
    WHATSAPP_VERIFY_TOKEN: str = "test-verify-token"

    # Configurações de Segurança
    ALLOWED_HOSTS: list[str] = ["*"]
    CORS_ORIGINS: list[str] = ["*"]

    # Configurações de Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 1000  # Alto para não interferir nos testes

    class Config:
        case_sensitive = True
        env_file = ".env.test"

    def __init__(self, **data):
        super().__init__(**data)

        if not self.SQLALCHEMY_DATABASE_URI and self.POSTGRES_DB:
            self.SQLALCHEMY_DATABASE_URI = (
                f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
            )

settings = TestSettings() 