import os
import re
import logging
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

# Constants
INPUT_FOLDER = "text_files_folder"
HEADER_FILE = 'header.txt'
SEPARATOR_FILE = 'separator.txt'
FOOTER_FILE = 'footer.txt'
OUTPUT_FILE = 'results.txt'
FILES_LIST_FILE = 'spisok_failov.txt'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ToolCheckerApp(App):
    def build(self):
        return ToolCheckerBoxLayout()

class ToolCheckerBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(ToolCheckerBoxLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'

        button = Button(text='Обработать файлы', size_hint=(None, None), size=(200, 50))
        button.bind(on_release=self.process_files)
        self.add_widget(button)

    def process_files(self, _):
        """Обработка файлов по заданным параметрам."""
        self.read_and_copy_files(
            INPUT_FOLDER, HEADER_FILE, SEPARATOR_FILE, FOOTER_FILE, OUTPUT_FILE, FILES_LIST_FILE
        )
        logger.info('Файлы обработаны!\n')

    def read_and_copy_files(
            self, input_folder, header_file, separator_file, footer_file, output_file, files_list_file):
        """
        Чтение и копирование файлов с учетом заданных параметров.

        :param input_folder: Папка с входными файлами.
        :param header_file: Путь к файлу с заголовком.
        :param separator_file: Путь к файлу с разделителем.
        :param footer_file: Путь к файлу с футером.
        :param output_file: Путь к файлу с результатами.
        :param files_list_file: Путь к файлу со списком обработанных файлов.
        """
        unique_texts = set()  # Множество для уникальных текстов
        processed_files = []  # Список для обработанных файлов

        def process_folder(folder):
            for root, _, files in os.walk(folder):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    if os.path.isfile(file_path) and file_name.lower().endswith('.mpf'):
                        processed_files.append(file_name)
                        with open(file_path, 'r', encoding='utf-8') as file:
                            # Чтение строк из файла
                            lines = file.readlines()

                            # Ищем тексты в формате T="текст" в строках, отсеянных от комментариев
                            for line in lines:
                                # Отсев строк, начинающихся с ';'
                                if not line.lstrip().startswith(';'):
                                    matches = re.findall(r'T="([^"]+)"', line, flags=re.DOTALL)
                                    unique_texts.update(match for match in matches)

        process_folder(input_folder)
        logger.info("Обработанные файлы: %s", processed_files)

        # Запись списка обработанных файлов
        with open(files_list_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(processed_files))

        # Чтение заголовка
        with open(header_file, 'r', encoding='utf-8') as file:
            header = file.read().strip()

        # Чтение разделителя
        with open(separator_file, 'r', encoding='utf-8') as file:
            separator = file.read().strip()

        # Чтение футера
        with open(footer_file, 'r', encoding='utf-8') as file:
            footer = file.read().strip()

        result = [header]
        if unique_texts:
            for i, text in enumerate(unique_texts, start=1):
                result.append(f'N{i} T="{text}"')
                result.append(separator)

        result.append(footer)

        # Запись результатов в файл
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(result))

        # Очистка списков после выполнения программы
        processed_files.clear()
        unique_texts.clear()

if __name__ == '__main__':
    ToolCheckerApp().run()
