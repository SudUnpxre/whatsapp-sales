FROM node:16-alpine

WORKDIR /app

# Copia os arquivos de configuração
COPY package*.json ./

# Instala as dependências
RUN npm install

# Copia o código fonte
COPY . .

# Expõe a porta da aplicação
EXPOSE 3000

# Inicia a aplicação
CMD ["npm", "start"] 