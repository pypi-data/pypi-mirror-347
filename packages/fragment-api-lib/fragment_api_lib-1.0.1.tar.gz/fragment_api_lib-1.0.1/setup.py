# Импорт недавно установленного пакета setuptools.
import setuptools

# Открытие README.md и присвоение его long_description.
with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

# Определение requests как requirements для того, чтобы этот пакет работал. Зависимости проекта.
requirements = ["requests>=2.31.0"]

# Функция, которая принимает несколько аргументов. Она присваивает эти значения пакету.
setuptools.setup()