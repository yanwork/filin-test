# Filin Console Application

![Python CI](https://github.com/yanwork/filin-test/workflows/Python%20CI/badge.svg)
![Build Docker Image](https://github.com/yanwork/filin-test/workflows/Build%20Docker%20Image/badge.svg)
![Publish Docker Image](https://github.com/yanwork/filin-test/workflows/Publish%20Docker%20Image/badge.svg)
![Release](https://img.shields.io/github/v/release/yanwork/filin-test)
![License](https://img.shields.io/github/license/yanwork/filin-test)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)

Консольное приложение с красивым форматированием, анимацией и поддержкой многоязычности.

## Описание

Это интерактивное консольное приложение предоставляет:
- Цветной вывод с анимацией
- Поддержку русского и английского языков
- Простые математические вычисления
- Красивое форматирование интерфейса

## Запуск с Docker

### Предварительные требования

- Docker

### Сборка и запуск

```bash
# Сборка образа
docker build -t filin-app .

# Запуск контейнера
docker run -it --rm filin-app
```


### Интерактивный режим

Поскольку приложение требует пользовательского ввода, важно запускать контейнер с флагами `-it` для интерактивного режима.

## Локальная разработка

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Запуск приложения

```bash
python main.py
```

### Запуск тестов

```bash
pytest
```

## Структура проекта

```
.
├── main.py              # Основной файл приложения
├── localization.py      # Модуль локализации
├── requirements.txt     # Зависимости Python
├── test_main.py        # Тесты
├── Dockerfile          # Конфигурация Docker
├── .dockerignore       # Исключения для Docker
└── README.md           # Документация
```

## CI/CD

Проект настроен с автоматической сборкой Docker образов через GitHub Actions:

### Автоматическая сборка
- **docker-build.yml** - автоматически собирает и тестирует Docker образ при каждом push в main
- **docker-publish.yml** - публикует образ в Docker Hub при создании релиза

### Настройка публикации в Docker Hub
Для публикации образов в Docker Hub необходимо добавить secrets в настройках репозитория:
- `DOCKERHUB_USERNAME` - имя пользователя Docker Hub
- `DOCKERHUB_TOKEN` - токен доступа Docker Hub

### Создание релиза для публикации
Для запуска публикации Docker образа:
1. Перейдите в раздел "Releases" на GitHub
2. Нажмите "Create a new release"
3. Выберите тег v1.0.0 (уже создан) или создайте новый
4. Заполните описание релиза
5. Нажмите "Publish release"

После публикации релиза автоматически запустится workflow docker-publish.yml

## Особенности Docker-контейнера

- Базовый образ: `python:3.11-slim`
- Рабочая директория: `/app`
- Поддержка интерактивного режима
- Оптимизированный размер образа
- Переменные окружения для корректной работы Python в контейнере
- Автоматическая сборка через GitHub Actions

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности смотрите в файле [LICENSE](LICENSE).
