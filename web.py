import sys
import os
import webbrowser
import re

# Определяем входные параметры
WEB_SOURCE = sys.argv[1]  # Путь к Python-файлу с кодом
WEB_TEMPLATE = sys.argv[2]  # Путь к HTML-шаблону
WEB_OUTPUT = sys.argv[3]  # Имя выходного HTML-файла

# Чтение Python-кода
with open(WEB_SOURCE, 'r', encoding='utf-8') as source_file:
    script = source_file.read()

# Определяем фрагмент, который нужно заменить (например, функцию print_board)
# Используем регулярные выражения для поиска нужной функции и замены
script = re.sub(
    r"async def print_board\(board\):.*?for row in reversed\(board\):.*?print\(\s*\" \"\s*,\s*\"  \"\s*.join\(row\)\).*?print\(\s*\"  \"\s*\+.*?map\(str, range\(1, 9\)\)\).*?print\(\)",
    """async def print_board(board):
    for row in reversed(board):
        print("  ", "  ".join(row))
        print()
    print("  " + "  ".join(map(str, range(1, 9))))
    print()""",
    script,
    flags=re.DOTALL
)

# Чтение HTML-шаблона
with open(WEB_TEMPLATE, 'r', encoding='utf-8') as template_file:
    template = template_file.read()

# Замена {script} на Python-код
output_html = template.replace("{script}", script)

# Получение директории для выходного файла
output_directory = os.path.dirname(WEB_OUTPUT)
if not output_directory:  # Если директория не указана, используем текущую директорию
    output_directory = os.getcwd()

# Создание выходной директории, если её нет
os.makedirs(output_directory, exist_ok=True)

# Запись выходного HTML-файла
output_path = os.path.join(output_directory, os.path.basename(WEB_OUTPUT))
with open(output_path, 'w', encoding='utf-8') as output_file:
    output_file.write(output_html)

# Открытие файла в браузере
webbrowser.open(f"file://{os.path.abspath(output_path)}")
