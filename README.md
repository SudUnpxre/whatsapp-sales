# WhatsApp Sales Automation

Sistema de automação de vendas via WhatsApp para pequenos negócios e vendedores autônomos.

## 🚀 Funcionalidades

- ✅ Automação de Respostas com IA (GPT-4)
- ✅ Catálogo de Produtos Interativo
- ✅ Automação de Follow-ups
- ✅ Gestão de Pedidos e Pagamentos
- ✅ Estatísticas e Relatórios
- ✅ Integração com Mercado Pago
- ✅ Dashboard Administrativo

## 🛠️ Tecnologias

- **Backend**: Python/FastAPI
- **Frontend**: React/Material-UI
- **Banco de Dados**: PostgreSQL
- **Cache**: Redis
- **IA**: OpenAI GPT-4
- **Pagamentos**: Mercado Pago
- **API**: WhatsApp Cloud API

## 📋 Pré-requisitos

- Python 3.9+
- Node.js 16+
- PostgreSQL 13+
- Redis
- Docker e Docker Compose (opcional)

## 🔧 Instalação

1. Clone o repositório
```bash
git clone https://github.com/[seu-usuario]/whatsapp-sales.git
cd whatsapp-sales
```

2. Configure o ambiente backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

4. Configure o banco de dados
```bash
alembic upgrade head
```

5. Inicie o servidor backend
```bash
uvicorn main:app --reload
```

6. Configure o frontend
```bash
cd ../frontend
npm install
npm start
```

## 🐳 Docker

Para rodar com Docker:

```bash
docker-compose up -d
```

## 📦 Estrutura do Projeto

```
whatsapp-sales/
├── backend/           # API FastAPI
│   ├── app/          # Código principal
│   ├── tests/        # Testes
│   └── alembic/      # Migrações
├── frontend/         # Aplicação React
└── docker/          # Configurações Docker
```

## 🔐 Configuração do WhatsApp

1. Crie uma conta no [Meta for Developers](https://developers.facebook.com/)
2. Configure um app do WhatsApp Business
3. Obtenha as credenciais necessárias
4. Configure no arquivo .env

## 💳 Configuração do Mercado Pago

1. Crie uma conta no [Mercado Pago](https://www.mercadopago.com.br/)
2. Obtenha as credenciais de teste/produção
3. Configure no arquivo .env

## 🤖 Configuração da OpenAI

1. Crie uma conta na [OpenAI](https://openai.com/)
2. Obtenha uma API key
3. Configure no arquivo .env

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Contribuição

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Faça o Commit das suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Faça o Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request 