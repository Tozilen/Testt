import json
import logging
import os
import re

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

# Импорт из plyer для работы с файловой системой
from plyer import filechooser

# Константы
SETTINGS_FILE = 'settings.json'

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ToolCheckerApp(App):
    def build(self):
        return ToolCheckerBoxLayout()

class MultiLineTextInput(TextInput):
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[0] == 13:
            self.insert_text('\n')
        else:
            super(MultiLineTextInput, self).keyboard_on_key_down(window, keycode, text, modifiers)

class FolderChooserPopup(Popup):
    def __init__(self, callback, **kwargs):
        super(FolderChooserPopup, self).__init__(**kwargs)
        self.file_chooser = FileChooserListView(path='/', dirselect=True)
        self.callback = callback
        self.content = self.file_chooser

class ToolCheckerBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(ToolCheckerBoxLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Форма для заголовка
        self.header_input = MultiLineTextInput(hint_text='Введите заголовок', multiline=True)
        self.add_widget(self.header_input)

        # Форма для разделителя
        self.separator_input = MultiLineTextInput(hint_text='Введите разделитель', multiline=True)
        self.add_widget(self.separator_input)

        # Форма для футера
        self.footer_input = MultiLineTextInput(hint_text='Введите футер', multiline=True)
        self.add_widget(self.footer_input)

        # Атрибуты для хранения значений
        self.header_value = ""
        self.separator_value = ""
        self.footer_value = ""
        self.selected_folder = ""

        # Загрузка сохраненных настроек при запуске
        self.load_settings()

        # Кнопка для выбора папки
        folder_button = Button(text='Выбрать папку', size_hint=(None, None), size=(200, 50))
        folder_button.bind(on_release=self.open_folder_chooser)
        self.add_widget(folder_button)

        # Кнопка для запуска обработки файлов
        process_button = Button(text='Обработать файлы', size_hint=(None, None), size=(200, 50))
        process_button.bind(on_release=self.process_files)
        self.add_widget(process_button)

    def open_folder_chooser(self, _):
        # Используем plyer для выбора диска
        folder_path = filechooser.choose_dir()
        if folder_path:
            self.set_selected_folder(folder_path[0])

    def set_selected_folder(self, selected_folder):
        self.selected_folder = selected_folder

    def process_files(self, _):
        """Обработка файлов по заданным параметрам."""
        # Сохранение значений из форм в атрибуты
        self.header_value = self.header_input.text
        self.separator_value = self.separator_input.text
        self.footer_value = self.footer_input.text

        # Сохранение настроек перед обработкой файлов
        self.save_settings()

        self.read_and_copy_files(
            self.selected_folder,
            self.header_value,
            self.separator_value,
            self.footer_value
        )
        logger.info('Файлы обработаны!\n')

    def read_and_copy_files(
            self, input_folder, header, separator, footer):
        unique_texts = set()

        def process_folder(folder):
            for root, dirs, files in os.walk(folder):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    if os.path.isfile(file_path) and file_name.lower().endswith('.mpf'):
                        with open(file_path, 'r', encoding='utf-8') as file:
                            lines = file.readlines()
                            for line in lines:
                                if not line.lstrip().startswith(';'):
                                    matches = re.findall(r'T="([^"]+)"', line, flags=re.DOTALL)
                                    unique_texts.update(match for match in matches)

        process_folder(input_folder)
        logger.info("Обработанные файлы в папке: %s", input_folder)

        result = [header]
        if unique_texts:
            for i, text in enumerate(unique_texts, start=1):
                result.append(f'N{i} T="{text}"')
                result.append(separator)

        result.append(footer)

        output_file = os.path.join(input_folder, 'ToolChecker.mpf')
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(result))

        unique_texts.clear()

    def save_settings(self):
        """Сохранение настроек в файл."""
        settings = {
            "Header": self.header_value,
            "Separator": self.separator_value,
            "Footer": self.footer_value,
            "SelectedFolder": self.selected_folder
        }

        with open(SETTINGS_FILE, 'w', encoding='utf-8') as file:
            json.dump(settings, file)

    def load_settings(self):
        """Загрузка сохраненных настроек из файла."""
        if os.path.isfile(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as file:
                settings = json.load(file)
                self.header_input.text = settings.get("Header", "")
                self.separator_input.text = settings.get("Separator", "")
                self.footer_input.text = settings.get("Footer", "")
                self.selected_folder = settings.get("SelectedFolder", "")

if __name__ == '__main__':
    ToolCheckerApp().run()
