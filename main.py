import os
import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Добавьте кнопку для запуска обработки файлов
        button = Button(text='Обработать файлы', size_hint=(None, None), size=(200, 50))
        button.bind(on_release=self.process_files)
        self.add_widget(button)

    def process_files(self, _):
        input_folder = "text_files_folder"  # папка с текстовыми файлами
        header_file = 'header.txt'  # файл со шапкой
        separator_file = 'separator.txt'  # файл с разделителем
        footer_file = 'footer.txt'  # файл с концом
        output_file = 'results.txt'  # файл для сохранения результатов
        files_list_file = 'spisok_failov.txt'  # файл для сохранения списка обработанных файлов

        # Вызываем функцию для обработки файлов
        self.read_and_copy_files(
            input_folder, header_file, separator_file, footer_file, output_file, files_list_file)

        print('Файлы обработаны!')

    def read_and_copy_files(
            self, input_folder, header_file, separator_file, footer_file, output_file, files_list_file):
        texts = []
        processed_files = []  # Новый список для хранения названий обработанных файлов

        # Функция для рекурсивного обхода файлов вложенных папок
        def process_folder(folder):
            for root, _dirs, files in os.walk(folder):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    if os.path.isfile(file_path) and file_name.lower().endswith('.mpf'):
                        processed_files.append(file_name)  # Добавляем название файла в список
                        with open(file_path, 'r', encoding='utf-8') as file:
                            # Используем регулярное выражение для поиска строк, начинающихся с 'T='
                            matches = re.findall(r'T=.*', file.read())
                            # Добавляем найденные строки в список texts
                            texts.extend(matches)

        # Вызываем функцию для обработки файлов
        process_folder(input_folder)
        print("Обработанные файлы:", processed_files)  # Выводим список обработанных файлов

        # Сохранение списка обработанных файлов в файле
        with open(files_list_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(processed_files))

        # Чтение файлов с шапкой, разделителем и концом
        with open(header_file, 'r', encoding='utf-8') as file:
            header = file.read().strip()

        with open(separator_file, 'r', encoding='utf-8') as file:
            separator = file.read().strip()

        with open(footer_file, 'r', encoding='utf-8') as file:
            footer = file.read().strip()

        # Формирование списка и запись его в файл результатов
        result = [header]
        if texts:
            for i, text in enumerate(texts, start=1):
                result.append(f'N{i} {text}')
                result.append(separator)
            result.pop()  # Убираем последний разделитель
        result.append(footer)

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(result))


class MyApp(App):
    def build(self):
        return MyBoxLayout()


if __name__ == '__main__':
    MyApp().run()
