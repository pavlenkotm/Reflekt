# 🌐 Web3 Reputation NFT

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Solidity](https://img.shields.io/badge/solidity-0.8.20-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Анализируй свою Web3-активность и получай персонализированный NFT-бейдж репутации!**

Web3 Reputation NFT — это децентрализованное приложение, которое сканирует ончейн-поведение пользователя (транзакции, NFT, участие в DAO, ENS и т.д.) и формирует репутационный NFT, визуализирующий его вклад в экосистему.

## ✨ Основные возможности

- 🔍 **Анализ кошелька**: Сканирование всей блокчейн-активности
- 📊 **Репутационный скоринг**: Оценка 0-100 баллов на основе множества факторов
- 🏆 **Система рангов**: 6 уровней от Novice до Legendary
- 🎨 **Генерация NFT**: Персонализированные бейджи с уникальным дизайном
- 📦 **IPFS хранилище**: Децентрализованное хранение изображений и метаданных
- 🚀 **Smart Contract**: ERC-721 контракт для минтинга NFT
- 📈 **Лидерборд**: Соревнуйтесь с другими пользователями
- 📤 **Экспорт профиля**: JSON-формат для DAO и рекрутинга

## 🎯 Критерии оценки репутации

| Критерий | Баллы | Описание |
|----------|-------|----------|
| 💎 Long-term Holder | +10 | Долгосрочное хранение активов |
| 🗳️ DAO Participation | +20 | Участие в управлении |
| 🎨 NFT Mints | +5 | Минтинг NFT |
| 📊 Transaction Volume | +15 | Общая активность |
| 🪙 Token Diversity | +10 | Разнообразие портфеля |
| 🏦 DeFi Usage | +15 | Использование DeFi |
| ⏰ Wallet Age | +10 | Возраст кошелька |
| 🏷️ ENS Ownership | +5 | Владение ENS |
| 💰 Balance | +5 | Текущий баланс |
| ⚠️ Frequent Swaps | -5 | Штраф за частый трейдинг |

## 🏗️ Архитектура

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Streamlit)                  │
│            Веб-интерфейс для пользователей              │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                  Backend (FastAPI)                       │
│          REST API для анализа и минтинга                │
└──┬──────────────┬──────────────┬──────────────┬─────────┘
   │              │              │              │
   ▼              ▼              ▼              ▼
┌────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│Wallet  │  │Reputation│  │  Badge   │  │   IPFS   │
│Scanner │  │Calculator│  │Generator │  │ Uploader │
└────┬───┘  └──────────┘  └──────────┘  └──────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│           Blockchain Layer (Ethereum/L2)                 │
│  RPC Nodes │ TheGraph │ Alchemy │ Smart Contracts       │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Быстрый старт

### Требования

- Python 3.9+
- Node.js 18+ (для smart contracts)
- Ethereum RPC endpoint (Alchemy/Infura)
- Pinata account (для IPFS)

### Установка

1. **Клонировать репозиторий**

```bash
git clone https://github.com/yourusername/web3-reputation-nft.git
cd web3-reputation-nft
```

2. **Установить Python зависимости**

```bash
pip install -r requirements.txt
```

3. **Настроить переменные окружения**

```bash
cp .env.example .env
# Отредактируйте .env и добавьте свои API ключи
```

4. **Установить зависимости для контрактов**

```bash
cd contracts
npm install
cd ..
```

### Конфигурация .env

```bash
# Blockchain RPC URLs
ETHEREUM_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY
OPTIMISM_RPC_URL=https://opt-mainnet.g.alchemy.com/v2/YOUR_API_KEY
BASE_RPC_URL=https://base-mainnet.g.alchemy.com/v2/YOUR_API_KEY

# TheGraph API
THEGRAPH_API_KEY=YOUR_THEGRAPH_API_KEY

# IPFS Configuration
PINATA_API_KEY=YOUR_PINATA_API_KEY
PINATA_SECRET_KEY=YOUR_PINATA_SECRET_KEY
PINATA_JWT=YOUR_PINATA_JWT
```

## 📖 Использование

### 1. Запуск Streamlit Frontend

```bash
streamlit run frontend/app.py
```

Откройте браузер: http://localhost:8501

### 2. Запуск FastAPI Backend

```bash
cd src
python api.py
```

API будет доступен на: http://localhost:8000
Документация: http://localhost:8000/docs

### 3. Деплой Smart Contract

```bash
cd contracts

# Компиляция
npx hardhat compile

# Деплой на тестовую сеть
npx hardhat run scripts/deploy.js --network sepolia

# Деплой на mainnet
npx hardhat run scripts/deploy.js --network optimism
```

## 📚 API Endpoints

### Анализ кошелька

```bash
POST /api/analyze
{
  "address": "0x..."
}
```

### Расчет репутации

```bash
POST /api/reputation
{
  "address": "0x..."
}
```

### Минт NFT

```bash
POST /api/mint
{
  "address": "0x..."
}
```

### Получить лидерборд

```bash
GET /api/leaderboard?limit=100
```

### Экспорт профиля

```bash
POST /api/export
{
  "address": "0x..."
}
```

## 🎨 Примеры бейджей

Система генерирует уникальные визуальные бейджи для каждого уровня:

- 🏆 **Legendary** (90-100): Золотой градиент
- ⭐ **Epic** (75-89): Фиолетовый градиент
- 💎 **Rare** (60-74): Голубой градиент
- 🔷 **Uncommon** (40-59): Зеленый градиент
- 🔹 **Common** (20-39): Бирюзовый градиент
- 🌱 **Novice** (0-19): Синий градиент

## 🔧 Структура проекта

```
web3-reputation-nft/
├── src/                      # Python модули
│   ├── wallet_scanner.py     # Анализ кошелька
│   ├── reputation_score.py   # Расчет репутации
│   ├── badge_generator.py    # Генерация NFT
│   ├── integrations.py       # Lens Protocol, DAO API
│   └── api.py               # FastAPI backend
├── contracts/                # Smart contracts
│   ├── ReputationNFT.sol    # ERC-721 контракт
│   ├── hardhat.config.js    # Hardhat конфиг
│   └── scripts/deploy.js    # Деплой скрипт
├── frontend/                 # Streamlit UI
│   └── app.py               # Главное приложение
├── data/                     # Данные приложения
│   ├── badges/              # Сгенерированные бейджи
│   ├── leaderboard.json     # Лидерборд
│   └── deployments/         # Адреса контрактов
├── tests/                    # Тесты
├── requirements.txt          # Python зависимости
├── .env.example             # Пример конфига
└── README.md                # Документация
```

## 🎯 Бонус-фичи

### 1. Интеграция с Lens Protocol

```python
from integrations import LensProtocolIntegration

lens = LensProtocolIntegration()
profile = lens.get_lens_profile("0x...")
lens_score = lens.calculate_lens_score(profile)
```

### 2. API для DAO рекрутинга

```python
from integrations import DAORecruitmentAPI

dao_api = DAORecruitmentAPI()
candidates = dao_api.search_candidates(
    min_score=70,
    min_dao_participation=2,
    required_badges=["DAO Voter"]
)
```

### 3. Продвинутый лидерборд

```python
from integrations import AdvancedLeaderboard

leaderboard = AdvancedLeaderboard()
top_dao_voters = leaderboard.get_top_by_category("dao_participation")
rising_stars = leaderboard.get_rising_stars(days=7)
```

## 🧪 Тестирование

```bash
# Тест Python модулей
pytest tests/

# Тест smart contracts
cd contracts
npx hardhat test
```

## 🛣️ Roadmap

- [x] Базовый анализ кошелька
- [x] Расчет репутационного скоринга
- [x] Генерация NFT бейджей
- [x] IPFS интеграция
- [x] Smart contract ERC-721
- [x] Streamlit frontend
- [x] FastAPI backend
- [ ] Интеграция с TheGraph
- [ ] Полная поддержка Lens Protocol
- [ ] Multi-chain поддержка (Polygon, Arbitrum)
- [ ] On-chain минтинг через frontend
- [ ] DAO governance для параметров скоринга
- [ ] NFT эволюция (обновление по времени)
- [ ] Мобильное приложение

## 🤝 Участие в разработке

Мы приветствуем вклад сообщества! Вот как вы можете помочь:

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add some AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📄 Лицензия

Distributed under the MIT License. See `LICENSE` for more information.

## 👥 Команда

- **Разработка**: Reflekt Team
- **Smart Contracts**: Solidity Engineers
- **Design**: UI/UX Team

## 📞 Контакты

- Website: [reflekt.app](https://reflekt.app)
- Twitter: [@ReflektApp](https://twitter.com/ReflektApp)
- Discord: [Join our community](https://discord.gg/reflekt)
- Email: team@reflekt.app

## 🙏 Благодарности

- [OpenZeppelin](https://openzeppelin.com/) - Smart contract библиотеки
- [Alchemy](https://www.alchemy.com/) - Blockchain infrastructure
- [Pinata](https://www.pinata.cloud/) - IPFS pinning service
- [TheGraph](https://thegraph.com/) - Blockchain indexing
- [Streamlit](https://streamlit.io/) - Frontend framework
- [FastAPI](https://fastapi.tiangolo.com/) - API framework

---

<p align="center">Made with ❤️ for the Web3 community</p>