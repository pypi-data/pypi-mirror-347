import random
import string

class PasswordGenerator:
    def __init__(self, length=12, use_uppercase=True, use_numbers=True, use_special_chars=True):
        self.length = length
        self.use_uppercase = use_uppercase
        self.use_numbers = use_numbers
        self.use_special_chars = use_special_chars

    def generate_password(self):
        # Базовый набор символов
        characters = string.ascii_lowercase  # Строчные буквы

        if self.use_uppercase:
            characters += string.ascii_uppercase  # Заглавные буквы
        if self.use_numbers:
            characters += string.digits  # Цифры
        if self.use_special_chars:
            characters += string.punctuation  # Специальные символы

        # Генерация пароля
        password = ''.join(random.choice(characters) for _ in range(self.length))
        return password

# Функция для генерации пароля
def generate_password(length=12, use_uppercase=True, use_numbers=True, use_special_chars=True):
    generator = PasswordGenerator(length, use_uppercase, use_numbers, use_special_chars)
    return generator.generate_password()