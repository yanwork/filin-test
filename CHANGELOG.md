# Changelog

## [1.1.0] - 2025-01-06

### Добавлено
- **Имя пользователя по умолчанию с таймаутом**: Добавлена функция автоматического использования имени по умолчанию, если пользователь не начинает вводить имя в течение 10 секунд.
- **Язык по умолчанию с таймаутом**: Добавлена функция автоматического выбора русского языка по умолчанию, если пользователь не выбирает язык в течение 10 секунд.

### Изменения
- Добавлена константа `INPUT_TIMEOUT = 10` для настройки времени ожидания ввода
- Создана функция `get_default_username()` для динамического определения имени по умолчанию в зависимости от выбранного языка:
  - Русский язык: "Пользователь"
  - Английский язык: "User"
- Добавлена функция `input_with_timeout()` для ввода с таймаутом с использованием многопоточности
- Обновлена функция `greet_user()` для использования нового механизма ввода с таймаутом
- Обновлена функция `select_language()` для использования таймаута при выборе языка
- Добавлены новые строки локализации:
  - `enter_name_with_default`: Приглашение к вводу с отображением имени по умолчанию
  - `using_default_name`: Сообщение об использовании имени по умолчанию
  - `using_default_language`: Сообщение об использовании языка по умолчанию
  - `timeout_message`: Сообщение о истечении времени ожидания

### Техническая реализация
- Использован модуль `threading` для неблокирующего ввода
- Использован модуль `queue` для безопасной передачи данных между потоками
- Реализован механизм определения начала ввода пользователя
- Добавлена поддержка многоязычности для имен по умолчанию

### Поведение приложения
1. При выборе языка отображается приглашение вида: "Ваш выбор (1/2): [1]: "
2. Если пользователь не выбирает язык в течение 10 секунд, автоматически используется русский язык
3. При запросе имени пользователя отображается приглашение вида: "Введите ваше имя [Пользователь]: "
4. Если пользователь не начинает вводить имя в течение 10 секунд, автоматически используется имя по умолчанию
5. Если пользователь начал вводить, ожидается завершение ввода без ограничения по времени
6. Если введена пустая строка, также используется имя по умолчанию
7. Отображается соответствующее сообщение при использовании значений по умолчанию

### Совместимость
- Все существующие функции сохранены без изменений
- Обратная совместимость полностью сохранена
- Поддержка всех существующих языков (русский, английский)
