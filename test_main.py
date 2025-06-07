import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

from main import (
    ConsoleUI, DisplayConfig, Calculator, 
    safe_input, greet_user
)


class TestConsoleUI(unittest.TestCase):
    """Тесты для класса ConsoleUI."""
    
    def setUp(self):
        """Настройка для каждого теста."""
        self.config = DisplayConfig(use_colors=False, use_animation=False)
        self.ui = ConsoleUI(self.config)
    
    def test_print_colored(self):
        """Тест метода print_colored."""
        with patch('builtins.print') as mock_print:
            self.ui.print_colored("Test message")
            mock_print.assert_called_once_with("Test message")
    
    def test_get_user_input(self):
        """Тест метода get_user_input."""
        with patch('builtins.input', return_value="Test input") as mock_input:
            result = self.ui.get_user_input("Enter")
            mock_input.assert_called_once_with("Enter: ")
            self.assertEqual(result, "Test input")
    
    def test_list_items_empty(self):
        """Тест метода list_items с пустым списком."""
        with patch('builtins.print') as mock_print:
            self.ui.list_items([])
            mock_print.assert_called_once()
    
    def test_list_items(self):
        """Тест метода list_items со списком элементов."""
        with patch('builtins.print') as mock_print:
            # Настраиваем mock для захвата вывода
            outputs = []
            mock_print.side_effect = lambda *args: outputs.append(' '.join(map(str, args)))
            
            self.ui.list_items(['яблоко', 'банан', 'вишня'])
            
            expected_output = [
                "Элементы в списке:",
                "- яблоко",
                "- банан",
                "- вишня"
            ]
            
            # Проверяем, что вывод соответствует ожидаемому
            self.assertEqual(len(outputs), len(expected_output))
            for actual, expected in zip(outputs, expected_output):
                self.assertEqual(actual, expected)
    
    def test_list_items_with_numbers(self):
        """Тест метода list_items со списком чисел."""
        with patch('builtins.print') as mock_print:
            outputs = []
            mock_print.side_effect = lambda *args: outputs.append(' '.join(map(str, args)))
            
            self.ui.list_items([1, 2, 3])
            
            expected_output = [
                "Элементы в списке:",
                "- 1",
                "- 2",
                "- 3"
            ]
            
            self.assertEqual(len(outputs), len(expected_output))
            for actual, expected in zip(outputs, expected_output):
                self.assertEqual(actual, expected)


class TestCalculator(unittest.TestCase):
    """Тесты для класса Calculator."""
    
    def setUp(self):
        """Настройка для каждого теста."""
        self.ui = MagicMock()
        self.calculator = Calculator(self.ui)
    
    def test_add(self):
        """Тест метода add."""
        # Тест с положительными числами
        self.assertEqual(self.calculator.add(5, 3, False), 8)
        
        # Тест с отрицательными числами
        self.assertEqual(self.calculator.add(-1, 1, False), 0)
        
        # Тест с нулями
        self.assertEqual(self.calculator.add(0, 0, False), 0)
        
        # Проверяем, что метод show_operation был вызван
        self.ui.show_operation.assert_called()


class TestHelperFunctions(unittest.TestCase):
    """Тесты для вспомогательных функций."""
    
    def test_safe_input_valid(self):
        """Тест функции safe_input с валидным вводом."""
        with patch('builtins.input', return_value="valid"):
            result = safe_input(
                lambda: input("Test: "),
                lambda x: x == "valid",
                "Error"
            )
            self.assertEqual(result, "valid")
    
    def test_safe_input_invalid_then_valid(self):
        """Тест функции safe_input с невалидным, а затем валидным вводом."""
        with patch('builtins.input', side_effect=["invalid", "valid"]):
            with patch('builtins.print') as mock_print:
                result = safe_input(
                    lambda: input("Test: "),
                    lambda x: x == "valid",
                    "Error"
                )
                mock_print.assert_called_once_with("Error")
                self.assertEqual(result, "valid")
    
    def test_greet_user(self):
        """Тест функции greet_user."""
        mock_ui = MagicMock()
        mock_ui.get_user_input.return_value = "Test User"
        
        with patch('main.safe_input', return_value="Test User") as mock_safe_input:
            result = greet_user(mock_ui)
            self.assertEqual(result, "Test User")
            mock_ui.print_colored.assert_called_once()


if __name__ == '__main__':
    unittest.main()
