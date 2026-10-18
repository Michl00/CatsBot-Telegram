# CatsBot (Aiogram + Redis + APScheduler)

An asynchronous Telegram bot that automatically sends random kitten photos to users at custom time intervals. Built with **Aiogram 3**, utilizing **Redis** for persistent user data storage and **APScheduler** for dynamic task scheduling.

## **Features**
* **Automated Mailing:** Periodic delivery of cute kitten pictures via external API integration.
* **Flexible Schedules:** Custom subscription intervals (e.g., every 1 or 2 hours, or manual hours input).
* **Persistent Storage:** Safe user profiles saving (subscription flags, timers, logs) inside a Redis database.
* **Resilience:** Automatic background scheduler recovery for all users immediately after bot or system reboots.
* **Safe Unsubscribing:** Complete background job destruction and profile wiping when a user decides to stop the bot.

## **Technologies**
* **Python 3.14**
* **Aiogram 3.x** (Telegram Bot framework)
* **Redis** (In-memory persistent storage inside Docker container)
* **APScheduler 3.x / 4.x** (Dynamic background task scheduling)
* **aiohttp** (Asynchronous HTTP requests to the Cat API)

---

## **Instruction for local deploy**

### 1. Clone repository
```bash
git clone https://github.com/Michl00/CatsBot-Telegram.git
cd CatsBot-Telegram
```

### 2. Virtual environment setting
```bash
python -m venv .venv
source .venv/Scripts/activate  # for Windows (Git Bash)
# source .venv/bin/activate    # for Linux / macOS
pip install -r requirements.txt
```

### 3. Environment configuration
Create a `.env` file in the root directory based on the `.env_example`:
```env
# BOT SETTINGS
BOT_TOKEN='' # your bot token

# LOGGING SETTINGS
LOG_FORMAT='[%(asctime)s] #%(levelname)8s %(filename)s:%(lineno)d - %(name)s - %(message)s'
LOG_LEVEL='DEBUG'
LOG_FILE='bot.log'

# DATABASE SETTINGS
DB_HOST='localhost'
DB_PORT=6379
DB_PASSWORD='' # your password for Redis
```

### 4. Starting Redis database (via Docker)
Make sure that Docker Desktop is up and running, then execute:
```bash
docker run --name cats-redis -p 6379:6379 -d redis:latest redis-server --appendonly yes --requirepass "your_redis_password_here"
```

### 5. Launching the Telegram Bot
```bash
python main.py
```

---

## **Available Bot Commands**

| Command | Description |
| :--- | :--- |
| `/start` | Welcome and initial help message |
| `/help` | Detailed guide on how to interact with the bot |
| `/time` | Open inline keyboard to choose or change mailing intervals |
| `/cat` | Instant single random cat delivery |
| `/stop` | Cancel subscription, delete background jobs, and wipe user data |

---

# CatsBot (Aiogram + Redis + APScheduler)

Асинхронный Telegram-бот для автоматической рассылки случайных фотографий котят с настраиваемым временным интервалом. Написан на **Aiogram 3**, использует базу данных **Redis** для персистентного хранения данных и **APScheduler** для динамического планирования фоновых задач.

## **Функционал**
* **Автоматическая рассылка:** Периодическая отправка картинок с котиками через интеграцию с внешним API.
* **Настройка расписания:** Выбор готовых интервалов рассылки (1 или 2 часа) либо ручной ввод любого количества часов через FSM-состояния.
* **Надежное хранилище:** Сохранение профилей пользователей (активность подписки, интервалы, время последней отправки) в Redis.
* **Отказоустойчивость:** Автоматическое восстановление всех активных таймеров рассылки для каждого пользователя из базы данных при перезапуске бота.
* **Управление подпиской:** Полная остановка фоновых задач и корректное удаление данных пользователя при отправке команды отписки.

## **Стек технологий**
* **Python 3.14**
* **Aiogram 3.x** (фреймворк для Telegram-ботов)
* **Redis** (высокопроизводительная БД в Docker-контейнере)
* **APScheduler 3.x / 4.x** (динамический планировщик фоновых задач)
* **aiohttp** (асинхронные HTTP-запросы к API с котиками)

---

## **Инструкция по локальному развертыванию**

### 1. Клонирование репозитория
```bash
git clone https://github.com/Michl00/CatsBot-Telegram.git
cd CatsBot-Telegram
```

### 2. Настройка виртуального окружения
```bash
python -m venv .venv
source .venv/Scripts/activate  # Для Windows (Git Bash)
# source .venv/bin/activate    # Для Linux / macOS
pip install -r requirements.txt
```

### 3. Настройка переменных окружения
Создайте файл `.env` в корневой директории по примеру из `.env_example`:
```env
# BOT SETTINGS
BOT_TOKEN='' # your bot token

# LOGGING SETTINGS
LOG_FORMAT='[%(asctime)s] #%(levelname)8s %(filename)s:%(lineno)d - %(name)s - %(message)s'
LOG_LEVEL='DEBUG'
LOG_FILE='bot.log'

# DATABASE SETTINGS
DB_HOST='localhost'
DB_PORT=6379
DB_PASSWORD='' # your password for Redis
```

### 4. Запуск базы данных Redis (через Docker)
Убедитесь, что у вас запущен Docker Desktop, и выполните команду для создания контейнера с включенной персистентностью:
```bash
docker run --name cats-redis -p 6379:6379 -d redis:latest redis-server --appendonly yes --requirepass "ваш_пароль_от_redis"
```

### 5. Запуск бота
```bash
python main.py
```

---

## **Список доступных команд бота**

| Команда | Описание |
| :--- | :--- |
| `/start` | Приветствие и вывод стартового сообщения |
| `/help` | Инструкция по использования функций бота |
| `/time` | Открыть инлайн-меню для выбора интервала рассылки |
| `/cat` | Получить одного случайного котика мгновенно |
| `/stop` | Полностью отписаться от рассылки и удалить свои данные из базы |
