"""
Модуль локализации для поддержки многоязычности в приложении.

Этот модуль предоставляет функции и структуры данных для управления
переводами текстов на разные языки.
"""

from enum import Enum
from typing import Dict, Any


class Language(Enum):
    """Поддерживаемые языки."""
    RUSSIAN = "ru"
    ENGLISH = "en"


# Словари с переводами для каждого языка
TRANSLATIONS: Dict[Language, Dict[str, Any]] = {
    Language.RUSSIAN: {
        # Общие строки
        "welcome_banner": "Добро пожаловать в программу",
        "farewell": "Спасибо за использование программы!",
        
        # Интерфейс
        "progress": "Прогресс",
        "result": "Результат",
        "result_with_colon": "Результат:",
        "calculation_result": "Результат вычисления:",
        "items_in_list": "Элементы в списке",
        
        # Ввод пользователя
        "enter_name": "Введите ваше имя",
        "enter_name_with_default": "Введите ваше имя [{default}]",
        "name_empty_error": "Имя не может быть пустым. Пожалуйста, введите ваше имя.",
        "invalid_input": "Некорректный ввод. Пожалуйста, попробуйте снова.",
        "hello": "Привет",
        "using_default_name": "Используем имя по умолчанию: {name}",
        "timeout_message": "Время ожидания истекло.",
        
        # Операции
        "calculating": "Вычисляем",
        "loading_items": "🔍 Загружаем список элементов...",
        
        # Примеры данных
        "fruits": ["яблоко", "банан", "вишня"],

        # Языковой выбор
        "select_language": "Выберите язык",
        "language_russian": "Русский",
        "language_english": "English",
        "language_prompt": "Ваш выбор (1/2): ",
        "invalid_language_choice": "Некорректный выбор. Пожалуйста, введите 1 или 2.",
        "using_default_language": "Используем язык по умолчанию: Русский"
    },
    
    Language.ENGLISH: {
        # Common strings
        "welcome_banner": "Welcome to the program",
        "farewell": "Thank you for using the program!",
        
        # Interface
        "progress": "Progress",
        "result": "Result",
        "result_with_colon": "Result:",
        "calculation_result": "Calculation result:",
        "items_in_list": "Items in the list",
        
        # User input
        "enter_name": "Enter your name",
        "enter_name_with_default": "Enter your name [{default}]",
        "name_empty_error": "Name cannot be empty. Please enter your name.",
        "invalid_input": "Invalid input. Please try again.",
        "hello": "Hello",
        "using_default_name": "Using default name: {name}",
        "timeout_message": "Timeout expired.",
        
        # Operations
        "calculating": "Calculating",
        "loading_items": "🔍 Loading list items...",
        
        # Sample data
        "fruits": ["apple", "banana", "cherry"],

        # Language selection
        "select_language": "Select language",
        "language_russian": "Russian",
        "language_english": "English",
        "language_prompt": "Your choice (1/2): ",
        "invalid_language_choice": "Invalid choice. Please enter 1 or 2.",
        "using_default_language": "Using default language: Russian"
    }
}


class Localizer:
    """Класс для управления локализацией текстов."""
    
    def __init__(self, language: Language = Language.RUSSIAN):
        """
        Инициализирует локализатор с указанным языком.
        
        Args:
            language: Язык для использования (по умолчанию русский)
        """
        self.language = language
    
    def get_text(self, key: str) -> str:
        """
        Возвращает локализованный текст по ключу.
        
        Args:
            key: Ключ для поиска в словаре переводов
            
        Returns:
            Локализованный текст
        """
        translations = TRANSLATIONS.get(self.language, TRANSLATIONS[Language.RUSSIAN])
        return translations.get(key, f"[Missing translation: {key}]")
    
    def get_list(self, key: str) -> list:
        """
        Возвращает локализованный список по ключу.
        
        Args:
            key: Ключ для поиска в словаре переводов
            
        Returns:
            Локализованный список
        """
        translations = TRANSLATIONS.get(self.language, TRANSLATIONS[Language.RUSSIAN])
        return translations.get(key, [])
    
    def set_language(self, language: Language) -> None:
        """
        Устанавливает язык для локализатора.
        
        Args:
            language: Новый язык
        """
        self.language = language


# Создаем глобальный экземпляр локализатора
localizer = Localizer()


def get_text(key: str) -> str:
    """
    Получает локализованный текст по ключу.
    
    Args:
        key: Ключ для поиска в словаре переводов
        
    Returns:
        Локализованный текст
    """
    return localizer.get_text(key)


def get_list(key: str) -> list:
    """
    Получает локализованный список по ключу.
    
    Args:
        key: Ключ для поиска в словаре переводов
        
    Returns:
        Локализованный список
    """
    return localizer.get_list(key)


def set_language(language: Language) -> None:
    """
    Устанавливает язык для локализации.
    
    Args:
        language: Новый язык
    """
    localizer.set_language(language)
