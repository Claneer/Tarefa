# 🐳 Guia de Instalação do Docker

## ⚠️ Importante

Este guia explica como instalar Docker e Docker Compose em diferentes sistemas operacionais para executar a aplicação completa em containers.

---

## 📋 Sistemas Operacionais

- [Linux (Ubuntu/Debian)](#linux-ubuntudebian)
- [Linux (CentOS/RHEL)](#linux-centosrhel)
- [macOS](#macos)
- [Windows](#windows)

---

## Linux (Ubuntu/Debian)

### 1. Remover versões antigas

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```

### 2. Instalar Docker

```bash
# Atualizar índice de pacotes
sudo apt-get update

# Instalar dependências
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Adicionar chave GPG oficial do Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Configurar repositório
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Atualizar índice de pacotes
sudo apt-get update

# Instalar Docker Engine
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 3. Instalar Docker Compose (standalone)

```bash
# Baixar versão mais recente
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Dar permissão de execução
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalação
docker-compose --version
```

### 4. Configurar permissões

```bash
# Adicionar seu usuário ao grupo docker
sudo usermod -aG docker $USER

# Aplicar mudanças (ou fazer logout/login)
newgrp docker
```

### 5. Verificar instalação

```bash
docker --version
docker-compose --version
docker run hello-world
```

---

## Linux (CentOS/RHEL)

### 1. Remover versões antigas

```bash
sudo yum remove docker \
    docker-client \
    docker-client-latest \
    docker-common \
    docker-latest \
    docker-latest-logrotate \
    docker-logrotate \
    docker-engine
```

### 2. Instalar Docker

```bash
# Instalar dependências
sudo yum install -y yum-utils

# Adicionar repositório Docker
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo

# Instalar Docker Engine
sudo yum install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Iniciar Docker
sudo systemctl start docker
sudo systemctl enable docker
```

### 3. Instalar Docker Compose

```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 4. Configurar permissões

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### 5. Verificar instalação

```bash
docker --version
docker-compose --version
docker run hello-world
```

---

## macOS

### Opção 1: Docker Desktop (Recomendado)

1. **Baixar Docker Desktop**
   - Acesse: https://docs.docker.com/desktop/install/mac-install/
   - Baixe o instalador para Mac (Intel ou Apple Silicon)

2. **Instalar**
   - Abra o arquivo `.dmg`
   - Arraste Docker para Applications
   - Execute Docker Desktop

3. **Verificar**
   ```bash
   docker --version
   docker-compose --version
   ```

### Opção 2: Homebrew

```bash
# Instalar Docker
brew install --cask docker

# Iniciar Docker Desktop
open /Applications/Docker.app

# Verificar
docker --version
docker-compose --version
```

---

## Windows

### Opção 1: Docker Desktop (Recomendado)

#### Requisitos
- Windows 10 64-bit: Pro, Enterprise, ou Education (Build 19041 ou superior)
- WSL 2 habilitado
- Hyper-V habilitado (opcional)

#### Instalação

1. **Habilitar WSL 2**
   ```powershell
   # Execute como Administrador no PowerShell
   wsl --install
   
   # Reinicie o computador
   ```

2. **Baixar Docker Desktop**
   - Acesse: https://docs.docker.com/desktop/install/windows-install/
   - Baixe o instalador

3. **Instalar**
   - Execute o instalador `.exe`
   - Siga as instruções
   - Reinicie se necessário

4. **Configurar**
   - Abra Docker Desktop
   - Vá em Settings > General
   - Marque "Use WSL 2 based engine"

5. **Verificar**
   ```powershell
   docker --version
   docker-compose --version
   ```

### Opção 2: Chocolatey

```powershell
# Execute como Administrador
choco install docker-desktop
```

---

## 🎯 Após Instalação

### Verificar se Docker está funcionando

```bash
# Verificar versão
docker --version
docker-compose --version

# Testar Docker
docker run hello-world

# Listar containers
docker ps

# Listar imagens
docker images
```

### Iniciar a Aplicação

```bash
# Navegar até o diretório do projeto
cd /app

# Dar permissões aos scripts (Linux/macOS)
chmod +x docker-start.sh docker-stop.sh docker-logs.sh

# Iniciar aplicação
./docker-start.sh
```

---

## 🐛 Solução de Problemas Comuns

### Docker daemon não está rodando

**Linux:**
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

**macOS/Windows:**
- Abra Docker Desktop

### Erro de permissão (Linux)

```bash
sudo usermod -aG docker $USER
newgrp docker
# ou fazer logout/login
```

### WSL 2 não instalado (Windows)

```powershell
# Execute como Administrador
wsl --install
wsl --set-default-version 2
```

### Porta já em uso

```bash
# Verificar o que está usando a porta
sudo lsof -i :8001  # Backend
sudo lsof -i :3000  # Frontend
sudo lsof -i :27017 # MongoDB

# Matar processo
sudo kill -9 <PID>

# Ou alterar portas no docker-compose.yml
```

### Erro "Cannot connect to Docker daemon"

```bash
# Linux
sudo systemctl restart docker

# Verificar status
sudo systemctl status docker
```

### Containers não iniciam

```bash
# Ver logs detalhados
docker-compose logs

# Reconstruir imagens
docker-compose build --no-cache

# Limpar tudo e recomeçar
docker-compose down -v
docker system prune -a
./docker-start.sh
```

---

## 📚 Recursos Adicionais

### Documentação Oficial

- **Docker**: https://docs.docker.com/
- **Docker Compose**: https://docs.docker.com/compose/
- **Docker Desktop**: https://docs.docker.com/desktop/

### Tutoriais

- **Get Started with Docker**: https://docs.docker.com/get-started/
- **Docker Compose Tutorial**: https://docs.docker.com/compose/gettingstarted/

### Comandos Úteis

```bash
# Ver containers rodando
docker ps

# Ver todos os containers
docker ps -a

# Ver imagens
docker images

# Remover container
docker rm <container_id>

# Remover imagem
docker rmi <image_id>

# Limpar sistema
docker system prune -a

# Ver uso de recursos
docker stats

# Ver logs de container
docker logs <container_name>

# Acessar shell do container
docker exec -it <container_name> bash
```

---

## ✅ Validação da Instalação

Execute este checklist após a instalação:

```bash
# 1. Verificar Docker
docker --version
# Saída esperada: Docker version 24.x.x ou superior

# 2. Verificar Docker Compose
docker-compose --version
# Saída esperada: Docker Compose version 2.x.x ou superior

# 3. Testar Docker
docker run hello-world
# Saída esperada: Hello from Docker!

# 4. Verificar daemon
docker info
# Deve mostrar informações do sistema Docker

# 5. Navegar até o projeto
cd /app

# 6. Verificar arquivos Docker
ls docker-compose.yml backend/Dockerfile frontend/Dockerfile
# Todos os arquivos devem existir

# 7. Iniciar aplicação
./docker-start.sh
# Deve construir e iniciar 3 containers

# 8. Verificar containers rodando
docker-compose ps
# Deve mostrar: mongodb, backend, frontend (UP)

# 9. Testar API
curl http://localhost:8001/api/
# Deve retornar JSON com informações da API

# 10. Testar frontend (navegador)
# Abrir: http://localhost:3000
```

### Saída Esperada

```bash
NAME                    IMAGE                   STATUS
api-pessoas-mongodb     mongo:7.0              Up
api-pessoas-backend     app-backend            Up
api-pessoas-frontend    app-frontend           Up
```

---

## 🎓 Próximos Passos

Após instalar e verificar o Docker:

1. ✅ Execute `./docker-start.sh`
2. ✅ Acesse http://localhost:8001/docs (Documentação da API)
3. ✅ Acesse http://localhost:3000 (Frontend)
4. ✅ Leia [DOCKER_SETUP.md](DOCKER_SETUP.md) para mais comandos
5. ✅ Explore [README_API.md](README_API.md) para usar a API

---

## 🆘 Precisa de Ajuda?

Se encontrar problemas:

1. **Verificar logs**: `./docker-logs.sh`
2. **Consultar**: [DOCKER_SETUP.md](DOCKER_SETUP.md)
3. **Reconstruir**: `docker-compose build --no-cache && docker-compose up -d`
4. **Limpar e reiniciar**: `docker-compose down -v && ./docker-start.sh`

---

**🐳 Docker instalado = Aplicação pronta para rodar!**

Execute: `./docker-start.sh`
