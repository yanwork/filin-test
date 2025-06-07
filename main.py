"""
Консольное приложение с красивым форматированием, анимацией и поддержкой многоязычности.

Этот модуль предоставляет функции для создания интерактивного консольного
приложения с цветным выводом, анимированными элементами, простыми
вычислениями и поддержкой разных языков.
"""

import sys
import time
import threading
import queue
from dataclasses import dataclass
from typing import List, Any, Optional, Callable, Union, TypeVar

# Сторонние библиотеки
from colorama import init, Fore, Style

# Локальные модули
from localization import Language, get_text, get_list, set_language

# Инициализация colorama
init()

# Константы для UI
PROGRESS_STEPS = 50
DEFAULT_PROGRESS_WIDTH = 20
ANIMATION_DELAY = 0.2
DEFAULT_PAUSE = 0.5

# Константы для пользователя
INPUT_TIMEOUT = 10  # секунд

def get_default_username() -> str:
    """Возвращает имя пользователя по умолчанию в зависимости от текущего языка."""
    from localization import localizer
    if localizer.language == Language.ENGLISH:
        return "User"
    else:
        return "Пользователь"

T = TypeVar('T')


@dataclass
class DisplayConfig:
    """Конфигурация отображения для консольного интерфейса."""
    use_colors: bool = True
    use_animation: bool = True
    progress_width: int = DEFAULT_PROGRESS_WIDTH
    animation_speed: float = ANIMATION_DELAY
    language: Language = Language.RUSSIAN


class ConsoleUI:
    """Класс для управления выводом в консоль с поддержкой цветов и анимации."""
    
    def __init__(self, config: DisplayConfig = None):
        """
        Инициализирует объект ConsoleUI.
        
        Args:
            config: Конфигурация отображения. Если не указана, используются значения по умолчанию.
        """
        self.config = config or DisplayConfig()
    
    def print_banner(self) -> None:
        """Выводит красивый баннер приветствия."""
        welcome_text = get_text("welcome_banner")
        banner = f"""
{Fore.CYAN if self.config.use_colors else ''}╔══════════════════════════════════════╗
║     {welcome_text}     ║
╚══════════════════════════════════════╝{Style.RESET_ALL if self.config.use_colors else ''}
"""
        print(banner)
    
    def print_colored(self, text: str, color: str = Fore.WHITE, bright: bool = False) -> None:
        """
        Выводит цветной текст.
        
        Args:
            text: Текст для вывода
            color: Цвет текста (из Fore)
            bright: Использовать ли яркий стиль
        """
        if self.config.use_colors:
            style = Style.BRIGHT if bright else ''
            print(f"{color}{style}{text}{Style.RESET_ALL}")
        else:
            print(text)
    
    def get_user_input(self, prompt: str, color: str = Fore.CYAN) -> str:
        """
        Запрашивает ввод от пользователя с цветным приглашением.
        
        Args:
            prompt: Текст приглашения
            color: Цвет приглашения
            
        Returns:
            Введенная пользователем строка
        """
        formatted_prompt = f"{color}{prompt}: {Style.RESET_ALL}" if self.config.use_colors else f"{prompt}: "
        return input(formatted_prompt)
    
    def show_progress(self, duration: float = 1.0, width: Optional[int] = None) -> None:
        """
        Показывает анимированный прогресс-бар.
        
        Args:
            duration: Длительность анимации в секундах
            width: Ширина прогресс-бара (если None, используется значение из конфигурации)
        """
        if width is None:
            width = self.config.progress_width
            
        progress_text = get_text("progress")
        
        for i in range(PROGRESS_STEPS + 1):
            filled = int(width * i / PROGRESS_STEPS)
            if self.config.use_colors:
                bar = f"{Fore.GREEN}{'█' * filled}{Fore.WHITE}{'░' * (width - filled)}"
                percent = i * 100 // PROGRESS_STEPS
                sys.stdout.write(f'\r{Fore.CYAN}{progress_text}: {Style.RESET_ALL}{bar} {percent}%')
            else:
                bar = '=' * filled + ' ' * (width - filled)
                percent = i * 100 // PROGRESS_STEPS
                sys.stdout.write(f'\r{progress_text}: [{bar}] {percent}%')
                
            sys.stdout.flush()
            time.sleep(duration / PROGRESS_STEPS)
            
        print(Style.RESET_ALL if self.config.use_colors else '')
    
    def list_items(self, items: List[Any], title: str = None) -> None:
        """
        Выводит список предоставленных элементов.
        
        Args:
            items: Список элементов для отображения
            title: Заголовок списка
        """
        if title is None:
            title = get_text("items_in_list")
            
        if not items:
            self.print_colored(f"{title}:", Fore.CYAN)
            return
            
        if self.config.use_colors:
            print(f"\n{Fore.CYAN}╭─ {title} ─╮{Style.RESET_ALL}")
            for item in items:
                if self.config.use_animation:
                    time.sleep(self.config.animation_speed)
                print(f"{Fore.WHITE}│ • {Style.BRIGHT}{item}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}╰{'─' * (len(title) + 2)}╯{Style.RESET_ALL}")
        else:
            print(f"{title}:")
            for item in items:
                if self.config.use_animation:
                    time.sleep(self.config.animation_speed)
                print(f"- {item}")
    
    def show_result(self, result: Any, prefix: str = None) -> None:
        """
        Выводит результат операции.
        
        Args:
            result: Результат для отображения
            prefix: Префикс перед результатом
        """
        if prefix is None:
            prefix = get_text("result_with_colon")
            
        if self.config.use_colors:
            print(f"\n{Fore.GREEN}✨ {prefix} {Style.BRIGHT}{result}{Style.RESET_ALL}")
        else:
            print(f"\n{prefix} {result}")
    
    def show_operation(self, operation: str) -> None:
        """
        Выводит информацию о выполняемой операции.
        
        Args:
            operation: Описание операции
        """
        if self.config.use_colors:
            print(f"\n{Fore.YELLOW}{operation}{Style.RESET_ALL}")
        else:
            print(f"\n{operation}")


class Calculator:
    """Класс для выполнения вычислений с визуальным отображением."""
    
    def __init__(self, ui: ConsoleUI):
        """
        Инициализирует калькулятор.
        
        Args:
            ui: Объект пользовательского интерфейса для вывода
        """
        self.ui = ui
    
    def add(self, a: Union[int, float], b: Union[int, float], show_animation: Optional[bool] = None) -> Union[int, float]:
        """
        Выполняет сложение двух чисел с визуальным эффектом.
        
        Args:
            a: Первое число
            b: Второе число
            show_animation: Показывать ли анимацию (если None, берется из конфигурации UI)
            
        Returns:
            Сумма двух чисел
        """
        calculating_text = get_text("calculating")
        self.ui.show_operation(f"{calculating_text}: {a} + {b}")
        
        if show_animation is None:
            show_animation = self.ui.config.use_animation
            
        if show_animation:
            self.ui.show_progress(0.8)
            
        return a + b


def input_with_timeout(prompt: str, timeout: float = INPUT_TIMEOUT, default: str = None) -> str:
    """
    Запрашивает ввод с таймаутом. Если пользователь не начинает вводить в течение указанного времени,
    возвращает значение по умолчанию.
    
    Args:
        prompt: Приглашение к вводу
        timeout: Время ожидания в секундах
        default: Значение по умолчанию
        
    Returns:
        Введенная строка или значение по умолчанию
    """
    result_queue = queue.Queue()
    input_started = threading.Event()
    
    def input_thread():
        """Поток для ввода данных."""
        try:
            # Показываем приглашение
            sys.stdout.write(prompt)
            sys.stdout.flush()
            
            # Ждем первый символ
            first_char = sys.stdin.read(1)
            if first_char:
                input_started.set()  # Сигнализируем, что ввод начался
                
                # Читаем остальную часть строки
                rest_of_line = sys.stdin.readline()
                full_input = first_char + rest_of_line.rstrip('\n\r')
                result_queue.put(full_input)
            else:
                result_queue.put("")
        except Exception as e:
            result_queue.put("")
    
    # Запускаем поток ввода
    thread = threading.Thread(target=input_thread, daemon=True)
    thread.start()
    
    # Ждем либо начала ввода, либо таймаута
    if input_started.wait(timeout):
        # Пользователь начал вводить, ждем завершения
        thread.join()
        try:
            return result_queue.get_nowait()
        except queue.Empty:
            return default
    else:
        # Таймаут истек
        if default == "1" and "[1]" in prompt:
            # Это выбор языка
            print(f"\n{get_text('timeout_message')} {get_text('using_default_language')}")
        elif default and default != "1":
            # Это имя пользователя
            print(f"\n{get_text('timeout_message')} {get_text('using_default_name').format(name=default)}")
        return default


def safe_input(prompt_func: Callable[[], str], 
               validation_func: Callable[[str], bool] = None, 
               error_message: str = None) -> str:
    """
    Безопасно запрашивает ввод с валидацией.
    
    Args:
        prompt_func: Функция, возвращающая приглашение к вводу
        validation_func: Функция валидации ввода (если None, принимается любой ввод)
        error_message: Сообщение об ошибке при неверном вводе
        
    Returns:
        Валидированный ввод пользователя
    """
    if error_message is None:
        error_message = get_text("invalid_input")
        
    while True:
        user_input = prompt_func()
        if validation_func is None or validation_func(user_input):
            return user_input
        print(error_message)


def greet_user(ui: ConsoleUI) -> str:
    """
    Запрашивает имя пользователя и здоровается с ним.
    Если пользователь не начинает вводить имя в течение 10 секунд,
    используется имя по умолчанию.
    
    Args:
        ui: Объект пользовательского интерфейса
        
    Returns:
        Имя пользователя
    """
    # Получаем имя по умолчанию для текущего языка
    default_username = get_default_username()
    
    # Получаем локализованные строки
    enter_name_template = get_text("enter_name_with_default")
    enter_name_prompt = enter_name_template.format(default=default_username)
    
    # Формируем цветное приглашение
    if ui.config.use_colors:
        formatted_prompt = f"{Fore.CYAN}{enter_name_prompt}: {Style.RESET_ALL}"
    else:
        formatted_prompt = f"{enter_name_prompt}: "
    
    # Запрашиваем ввод с таймаутом
    name = input_with_timeout(formatted_prompt, INPUT_TIMEOUT, default_username)
    
    # Если имя пустое, используем значение по умолчанию
    if not name.strip():
        name = default_username
        ui.print_colored(get_text("using_default_name").format(name=name), Fore.YELLOW)
    
    # Приветствуем пользователя
    hello_text = get_text("hello")
    ui.print_colored(f"{hello_text}, {name}!", Fore.GREEN, bright=True)
    return name


def select_language() -> Language:
    """
    Запрашивает у пользователя выбор языка с таймаутом.
    Если пользователь не выбирает язык в течение 10 секунд, 
    используется русский язык по умолчанию.
    
    Returns:
        Выбранный язык
    """
    print(get_text("select_language"))
    print(f"1. {get_text('language_russian')}")
    print(f"2. {get_text('language_english')}")
    
    # Формируем приглашение с указанием языка по умолчанию
    prompt = f"{get_text('language_prompt')} [1]: "
    
    while True:
        choice = input_with_timeout(prompt, INPUT_TIMEOUT, "1")
        
        if choice == "1" or choice.strip() == "":
            return Language.RUSSIAN
        elif choice == "2":
            return Language.ENGLISH
        else:
            print(get_text("invalid_language_choice"))
            # Для повторного запроса используем обычный input без таймаута
            prompt = get_text("language_prompt")


def main() -> None:
    """Организует поток выполнения программы."""
    # Выбор языка
    language = select_language()
    set_language(language)
    
    # Создаем конфигурацию и UI
    config = DisplayConfig(use_colors=True, use_animation=True, language=language)
    ui = ConsoleUI(config)
    calculator = Calculator(ui)
    
    # Основной поток программы
    ui.print_banner()
    time.sleep(DEFAULT_PAUSE)  # Небольшая пауза для эффекта
    
    name = greet_user(ui)
    
    result = calculator.add(5, 3)
    calculation_result = get_text("calculation_result")
    ui.show_result(result, calculation_result)
    
    loading_text = get_text("loading_items")
    ui.show_operation(loading_text)
    ui.show_progress(0.5)
    ui.list_items(get_list("fruits"))
    
    farewell_text = get_text("farewell")
    ui.print_colored(f"\n👋 {farewell_text}", Fore.CYAN)


if __name__ == "__main__":
    main()
