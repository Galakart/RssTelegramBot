# RSS Telegram Bot

[![Linting Python files](https://github.com/Galakart/RssTelegramBot/actions/workflows/lint-develop-job.yml/badge.svg)](https://github.com/Galakart/RssTelegramBot/actions/workflows/lint-develop-job.yml) [![Deploy on Docker](https://github.com/Galakart/RssTelegramBot/actions/workflows/deploy-on-master-job.yml/badge.svg)](https://github.com/Galakart/RssTelegramBot/actions/workflows/deploy-on-master-job.yml)

### Описание
Telegram бот, который выкачивает и отправляет посты из RSS-лент новостей.

### Требования
- Linux
- Docker Compose

### Установка
1. В Telegram создать себе нового бота. Для этого нужно написать боту https://t.me/BotFather, отправить ему команду /newbot и задать имя бота.
В ответ получим api-токен.

2. Склонировать себе репозиторий
```bash
git clone https://github.com/Galakart/RssTelegramBot.git
```

3. Зайти в полученную папку и скопировать файл настроек
```bash
cd RssTelegramBot
cp env_example .env
```

4. Отредактировать этот файл настроек, в частности в поле BOT_TOKEN обязательно вписать api-токен созданного бота. Остальные параметры поменять по желанию

### Запуск
Старт бота:
```bash
docker compose up -d
```

Остановка:
```bash
docker compose down
```

### Использование
После команды /start бот автоматически регистрирует первого написавшего ему пользователя, после чего переходит в главное меню.

В главном меню бота доступны две кнопки:
- 📃Мои ленты
- 📫Подписаться на новую

После нажатия на "Подписаться на новую", бот запросит ссылку на RSS-ленту, после чего проверит её валидность и сохранит себе. 

Сразу после добавления ленты бот загрузит последние 5 её постов и отправит их пользователю. В дальнейшем каждые 12 часов (время фиксировано) бот будет проверять наличие новых постов в ленте, и отправлять их.

Проверить список своих подписок на RSS-ленты и удалить их - можно в пункте меню "Мои ленты".

#### Запуск в dev-окружении (для программистов)
Пересборка проекта, старт бота и открытие порта БД для внешнего доступа:
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build
```

Запуск только контейнера с БД (для её просмотра, или для создания миграций):
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d db
```

Остановка с удалением неиспользуемых docker images:
```bash
docker compose down | yes | docker image prune
```
