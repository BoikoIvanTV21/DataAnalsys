import os

class FileManager:
    def __init__(self, filename, mode='r'):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        if 'r' in self.mode and not any(m in self.mode for m in ('w', 'a', 'x')):
            try:
                open(self.filename, 'r').close()
            except FileNotFoundError:
                open(self.filename, 'w').close()
        if not os.access(os.path.dirname(self.filename) or '.', os.W_OK):
            raise PermissionError(f"Недостатньо прав для запису в: {self.filename}")
        self.file = open(self.filename, self.mode, encoding='utf-8')
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()
        return False

def get_filename():
    choice = input("Введіть 1 для вибору власного шляху або 2 для використання стандартного пресету: ")
    if choice == '1':
        path = input("Введіть шлях до файлу: ")
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        return path
    default_path = os.path.join(os.getcwd(), "default.txt")
    print(f"Використовується стандартний файл: {default_path}")
    return default_path

filename = get_filename()
try:
    with FileManager(filename, "a") as file:
        file.write("Цей текст буде додано до файлу.\n")
except PermissionError as e:
    print(e)
