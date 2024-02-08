import os

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

    def process_files(self, instance):
        input_folder = "text_files_folder"  # папка с текстовыми файлами
        header_file = 'header.txt'  # файл со шапкой
        separator_file = 'separator.txt'  # файл с разделителем
        footer_file = 'footer.txt'  # файл с концом
        output_file = 'results.txt'  # файл для сохранения результатов

        # Вызываем функцию для обработки файлов
        self.read_and_copy_files(input_folder, header_file, separator_file, footer_file, output_file)

        print('Файлы обработаны!')

    def read_and_copy_files(self, input_folder, header_file, separator_file, footer_file, output_file):
        texts = []

        # Функция для рекурсивного обхода файлов вложенных папок
        def process_folder(folder):
            for root, dirs, files in os.walk(folder):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    if os.path.isfile(file_path) and file_name.lower().endswith('.mpf'):
                        with open(file_path, 'r', encoding='utf-8') as file:
                            # Читаем все строки из файла
                            lines = file.readlines()
                            # Добавляем все строки, начинающиеся с 'T=', в список texts
                            for line in lines:
                                if line.startswith('T='):
                                    texts.append(line)





        # Вызываем функцию для обработки файлов
        process_folder(input_folder)
        print(texts)

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
            for i, text in enumerate(texts):
                result.append('N' + str(i + 1) + text)
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