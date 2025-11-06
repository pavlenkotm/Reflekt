# Contributing to Web3 Reputation NFT

Спасибо за интерес к участию в проекте! Мы рады вашему вкладу.

## 🚀 Как участвовать

### Reporting Issues

Если вы нашли баг или у вас есть предложение:

1. Проверьте, нет ли уже такого issue
2. Создайте новый issue с подробным описанием
3. Используйте шаблоны для bug report или feature request

### Pull Requests

1. Fork репозитория
2. Создайте feature branch из `main`:
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. Внесите изменения:
   - Следуйте code style проекта
   - Добавьте тесты для новой функциональности
   - Обновите документацию при необходимости

4. Commit с понятным сообщением:
   ```bash
   git commit -m "Add: new reputation scoring algorithm"
   ```

5. Push в ваш fork:
   ```bash
   git push origin feature/amazing-feature
   ```

6. Создайте Pull Request на GitHub

## 📝 Code Style

### Python

- Следуйте PEP 8
- Используйте type hints
- Документируйте функции с помощью docstrings
- Максимальная длина строки: 100 символов

Пример:
```python
def calculate_score(wallet_data: Dict[str, Any]) -> float:
    """
    Calculate reputation score from wallet data.

    Args:
        wallet_data: Dictionary containing wallet metrics

    Returns:
        Reputation score between 0 and 100
    """
    pass
```

### Solidity

- Следуйте Solidity Style Guide
- Используйте NatSpec для документации
- Все контракты должны быть протестированы

### Commit Messages

Используйте conventional commits:

- `feat:` новая функциональность
- `fix:` исправление бага
- `docs:` изменения в документации
- `style:` форматирование, отсутствие изменений в коде
- `refactor:` рефакторинг кода
- `test:` добавление тестов
- `chore:` обновление зависимостей и т.д.

Примеры:
```
feat: add Lens Protocol integration
fix: resolve IPFS upload timeout issue
docs: update API endpoint documentation
```

## 🧪 Testing

Перед созданием PR убедитесь, что:

```bash
# Python тесты проходят
pytest tests/

# Smart contract тесты проходят
cd contracts && npx hardhat test

# Код соответствует стилю
flake8 src/
black --check src/
```

## 🎯 Приоритетные области

Мы особенно приветствуем вклад в:

- TheGraph subgraph интеграцию
- Multi-chain поддержку (Polygon, Arbitrum)
- Улучшение UI/UX
- Оптимизацию gas для контрактов
- Новые критерии репутации
- Тесты и документацию

## 💬 Вопросы?

- Discord: [discord.gg/reflekt]
- Discussions: GitHub Discussions
- Email: dev@reflekt.app

Спасибо за ваш вклад! 🙏
