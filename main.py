import os
import re
import logging
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

# Константы
INPUT_FOLDER = "text_files_folder"
OUTPUT_FILE = 'results.txt'
FILES_LIST_FILE = 'spisok_failov.txt'
SETTINGS_FILE = 'settings.txt'  # Файл для сохранения настроек

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiLineTextInput(TextInput):
    """Класс для создания многострочного ввода."""
    pass

class ToolCheckerApp(App):
    def build(self):
        return ToolCheckerBoxLayout()

class ToolCheckerBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(ToolCheckerBoxLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Форма для заголовка
        self.header_input = MultiLineTextInput(hint_text='Введите заголовок')
        self.add_widget(self.header_input)

        # Форма для разделителя
        self.separator_input = MultiLineTextInput(hint_text='Введите разделитель')
        self.add_widget(self.separator_input)

        # Форма для футера
        self.footer_input = MultiLineTextInput(hint_text='Введите футер')
        self.add_widget(self.footer_input)

        # Атрибуты для хранения значений
        self.header_value = ""
        self.separator_value = ""
        self.footer_value = ""

        # Загрузка сохраненных настроек при запуске
        self.load_settings()

        # Кнопка для запуска обработки файлов
        button = Button(text='Обработать файлы', size_hint=(None, None), size=(200, 50))
        button.bind(on_release=self.process_files)
        self.add_widget(button)

    def process_files(self, _):
        """Обработка файлов по заданным параметрам."""
        # Сохранение значений из форм в атрибуты
        self.header_value = self.header_input.text
        self.separator_value = self.separator_input.text
        self.footer_value = self.footer_input.text

        # Сохранение настроек перед обработкой файлов
        self.save_settings()

        self.read_and_copy_files(
            INPUT_FOLDER,
            self.header_value,
            self.separator_value,
            self.footer_value,
            OUTPUT_FILE,
            FILES_LIST_FILE
        )
        logger.info('Файлы обработаны!\n')

    def read_and_copy_files(
            self, input_folder, header, separator, footer, output_file, files_list_file):
        unique_texts = set()
        processed_files = []

        def process_folder(folder):
            for root, _, files in os.walk(folder):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    if os.path.isfile(file_path) and file_name.lower().endswith('.mpf'):
                        processed_files.append(file_name)
                        with open(file_path, 'r', encoding='utf-8') as file:
                            lines = file.readlines()
                            for line in lines:
                                if not line.lstrip().startswith(';'):
                                    matches = re.findall(r'T="([^"]+)"', line, flags=re.DOTALL)
                                    unique_texts.update(match for match in matches)

        process_folder(input_folder)
        logger.info("Обработанные файлы: %s", processed_files)

        with open(files_list_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(processed_files))

        result = [header]
        if unique_texts:
            for i, text in enumerate(unique_texts, start=1):
                result.append(f'N{i} T="{text}"')
                result.append(separator)

        result.append(footer)

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(result))

        processed_files.clear()
        unique_texts.clear()

    def save_settings(self):
        """Сохранение настроек в файл."""
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as file:
            file.write(f"Header: {self.header_value}\n")
            file.write(f"Separator: {self.separator_value}\n")
            file.write(f"Footer: {self.footer_value}\n")

    def load_settings(self):
        """Загрузка сохраненных настроек из файла."""
        if os.path.isfile(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as file:
                for line in file:
                    parts = line.strip().split(': ')
                    if len(parts) == 2:
                        key, value = parts
                        if key == "Header":
                            self.header_input.text = value
                        elif key == "Separator":
                            self.separator_input.text = value
                        elif key == "Footer":
                            self.footer_input.text = value

if __name__ == '__main__':
    ToolCheckerApp().run()
