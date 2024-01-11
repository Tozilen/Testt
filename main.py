import os

def read_and_copy_files(input_folder, header_file, separator_file, footer_file, output_file):
    texts = []

    # Перебор файлов в папке с текстовыми файлами
    for file_name in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith('T=') and line not in texts:
                        texts.append(line)

    # Чтение файлов с шапкой, разделителем и концом
    with open(header_file, 'r') as file:
        header = file.read().strip()

    with open(separator_file, 'r') as file:
        separator = file.read().strip()

    with open(footer_file, 'r') as file:
        footer = file.read().strip()

    # Формирование списка и запись его в файл результатов
    result = [header]
    if texts:
        result.append(texts[0])
        for text in texts[1:]:
            result.append(separator)
            result.append(text)
    result.append(footer)

    with open(output_file, 'w') as file:
        file.write('\n'.join(result))


# Пример использования функции
input_folder = 'папка_с_файлами'  # папка с текстовыми файлами
header_file = 'header.txt'  # файл со шапкой
separator_file = 'separator.txt'  # файл с разделителем
footer_file = 'footer.txt'  # файл с концом
output_file = 'результаты.txt'  # файл для сохранения результатов

read_and_copy_files(input_folder, header_file, separator_file, footer_file, output_file)