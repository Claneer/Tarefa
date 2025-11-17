FROM node:18-alpine

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos de dependências
COPY package.json yarn.lock ./

# Instala dependências
RUN yarn install --frozen-lockfile

# Copia código da aplicação
COPY . .

# Expõe porta do frontend
EXPOSE 3000

# Comando para iniciar em modo desenvolvimento
CMD ["yarn", "start"]
