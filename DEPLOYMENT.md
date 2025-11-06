# 🚀 Deployment Guide

Руководство по развертыванию Web3 Reputation NFT на различных окружениях.

## 📋 Содержание

1. [Local Development](#local-development)
2. [Smart Contract Deployment](#smart-contract-deployment)
3. [Backend Deployment](#backend-deployment)
4. [Frontend Deployment](#frontend-deployment)
5. [Production Checklist](#production-checklist)

## 🏠 Local Development

### Шаг 1: Установка зависимостей

```bash
# Python зависимости
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
pip install -r requirements.txt

# Smart contract зависимости
cd contracts
npm install
cd ..
```

### Шаг 2: Настройка окружения

```bash
# Создать .env файл
cp .env.example .env

# Заполнить необходимые переменные:
# - ETHEREUM_RPC_URL (получить на Alchemy/Infura)
# - PINATA_JWT (зарегистрироваться на Pinata.cloud)
# - Остальные по необходимости
```

### Шаг 3: Запуск локального блокчейна (опционально)

```bash
cd contracts
npx hardhat node
# Запустится локальная нода на порту 8545
```

### Шаг 4: Запуск приложения

```bash
# Терминал 1: Backend API
cd src
python api.py

# Терминал 2: Frontend
streamlit run frontend/app.py
```

## 📝 Smart Contract Deployment

### Тестовые сети

#### Sepolia (Ethereum Testnet)

```bash
cd contracts

# Получить тестовые ETH: https://sepoliafaucet.com/

# Деплой
npx hardhat run scripts/deploy.js --network sepolia

# Верификация
npx hardhat verify --network sepolia DEPLOYED_CONTRACT_ADDRESS
```

#### Optimism Sepolia

```bash
# Получить тестовые ETH на Optimism Sepolia
# Bridge: https://app.optimism.io/bridge

npx hardhat run scripts/deploy.js --network optimismSepolia
```

#### Base Sepolia

```bash
# Получить тестовые ETH на Base Sepolia
# Faucet: https://www.coinbase.com/faucets/base-ethereum-sepolia-faucet

npx hardhat run scripts/deploy.js --network baseSepolia
```

### Mainnet Deployment

⚠️ **ВАЖНО**: Деплой на mainnet стоит реальных денег. Убедитесь, что:
- Контракт полностью протестирован
- Проведен аудит безопасности
- Есть достаточно ETH для gas
- Все параметры проверены

#### Ethereum Mainnet

```bash
# Убедитесь, что PRIVATE_KEY в .env - это кошелек с ETH
npx hardhat run scripts/deploy.js --network mainnet

# Верификация на Etherscan
npx hardhat verify --network mainnet DEPLOYED_CONTRACT_ADDRESS
```

#### Optimism Mainnet

```bash
npx hardhat run scripts/deploy.js --network optimism

# Верификация на Optimistic Etherscan
npx hardhat verify --network optimism DEPLOYED_CONTRACT_ADDRESS
```

#### Base Mainnet

```bash
npx hardhat run scripts/deploy.js --network base

# Верификация на BaseScan
npx hardhat verify --network base DEPLOYED_CONTRACT_ADDRESS
```

### После деплоя

1. Сохраните адрес контракта в `.env`:
```bash
CONTRACT_ADDRESS=0x...
```

2. Сохраните информацию о деплое:
```bash
# Автоматически сохраняется в data/deployments/{network}.json
cat data/deployments/optimism.json
```

## 🖥️ Backend Deployment

### Вариант 1: Railway

```bash
# 1. Установить Railway CLI
npm i -g @railway/cli

# 2. Логин
railway login

# 3. Инициализация
railway init

# 4. Добавить переменные окружения
railway variables set ETHEREUM_RPC_URL=...
railway variables set PINATA_JWT=...

# 5. Деплой
railway up
```

### Вариант 2: Render

```bash
# 1. Создать render.yaml в корне проекта
cat > render.yaml << EOF
services:
  - type: web
    name: web3-reputation-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: cd src && python api.py
    envVars:
      - key: ETHEREUM_RPC_URL
        sync: false
      - key: PINATA_JWT
        sync: false
EOF

# 2. Push в Git
# 3. Подключить репозиторий на render.com
# 4. Настроить env variables в dashboard
```

### Вариант 3: Docker

```bash
# Создать Dockerfile
cat > Dockerfile << EOF
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "src/api.py"]
EOF

# Собрать образ
docker build -t web3-reputation-api .

# Запустить
docker run -p 8000:8000 --env-file .env web3-reputation-api
```

### Вариант 4: VPS (Ubuntu)

```bash
# На сервере
sudo apt update
sudo apt install python3.9 python3-pip nginx

# Клонировать репозиторий
git clone https://github.com/yourusername/web3-reputation-nft.git
cd web3-reputation-nft

# Установить зависимости
pip3 install -r requirements.txt

# Настроить systemd service
sudo nano /etc/systemd/system/web3-reputation.service

# Содержимое:
[Unit]
Description=Web3 Reputation API
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/web3-reputation-nft
Environment="PATH=/usr/bin"
ExecStart=/usr/bin/python3 /path/to/web3-reputation-nft/src/api.py

[Install]
WantedBy=multi-user.target

# Запустить сервис
sudo systemctl enable web3-reputation
sudo systemctl start web3-reputation

# Настроить Nginx
sudo nano /etc/nginx/sites-available/web3-reputation

# Содержимое:
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Активировать конфигурацию
sudo ln -s /etc/nginx/sites-available/web3-reputation /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🎨 Frontend Deployment

### Streamlit Cloud (Рекомендуется)

```bash
# 1. Push код в GitHub
git push origin main

# 2. Перейти на streamlit.io/cloud
# 3. Подключить GitHub репозиторий
# 4. Указать:
#    - Main file: frontend/app.py
#    - Python version: 3.9
# 5. Добавить secrets (эквивалент .env):
#    Settings > Secrets > Edit Secrets

# Пример secrets.toml:
ETHEREUM_RPC_URL = "https://..."
PINATA_JWT = "..."
```

### Vercel (с API)

```bash
# vercel.json
{
  "builds": [
    {
      "src": "frontend/app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "frontend/app.py"
    }
  ]
}

# Деплой
vercel --prod
```

## ✅ Production Checklist

### Безопасность

- [ ] Все API ключи в environment variables
- [ ] PRIVATE_KEY никогда не коммитится в Git
- [ ] CORS настроен правильно (не allow all origins)
- [ ] Rate limiting настроен на API
- [ ] Smart contract прошел аудит
- [ ] Используется HTTPS

### Производительность

- [ ] Кэширование включено для API
- [ ] Database connection pooling (если используется БД)
- [ ] CDN для статических файлов
- [ ] Compression включен (gzip)
- [ ] Image optimization для NFT badges

### Мониторинг

- [ ] Error tracking (Sentry)
- [ ] Analytics (Google Analytics / Mixpanel)
- [ ] Uptime monitoring (UptimeRobot)
- [ ] Log aggregation (LogDNA / Papertrail)

### Инфраструктура

- [ ] Backup strategy для данных
- [ ] Auto-scaling настроен
- [ ] Health check endpoints работают
- [ ] Load balancer настроен (для высокой нагрузки)

### Документация

- [ ] API документация обновлена
- [ ] README актуален
- [ ] Changelog ведется
- [ ] Комментарии в коде

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest tests/

      - name: Deploy to production
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
        run: |
          # Ваш скрипт деплоя
          echo "Deploying..."
```

## 📊 Monitoring & Logging

### Sentry Integration

```python
# src/api.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0,
)
```

### Logging

```python
# src/api.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

## 🆘 Troubleshooting

### Проблема: "Connection refused" при подключении к RPC

**Решение**: Проверьте:
- Правильность RPC URL в .env
- Валидность API ключа
- Rate limits на вашем RPC провайдере

### Проблема: IPFS upload fails

**Решение**:
- Проверьте PINATA_JWT токен
- Убедитесь, что у вас есть pinning quota
- Проверьте размер файла (<100MB для free tier)

### Проблема: Gas estimation failed

**Решение**:
- Убедитесь, что у деплоера достаточно ETH
- Проверьте правильность network в hardhat.config.js
- Увеличьте gas limit в deploy script

## 📞 Поддержка

Если возникли проблемы с деплоем:
- Создайте issue на GitHub
- Напишите в Discord: [discord.gg/reflekt]
- Email: support@reflekt.app

---

Happy Deploying! 🚀
