import os

def search_text(filepath):
    results = []
    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith('T='):
                text_value = line.split('T=')[1].strip()
                if text_value not in results:  # Исключаем повторяющиеся значения
                    results.append(text_value)
    return results

def save_to_file(results, output_file, header_file, separator_file, footer_file):
    with open(output_file, 'w') as file:
        if os.path.isfile(header_file):
            with open(header_file, 'r') as header:
                file.write(header.read() + '\n')

        for i, result in enumerate(results):
            if os.path.isfile(separator_file):
                with open(separator_file, 'r') as separator:
                    file.write(separator.read() + '\n')

            file.write(result + '\n')

        if os.path.isfile(footer_file):
            with open(footer_file, 'r') as footer:
                file.write(footer.read() + '\n')

    print("Результаты сохранены в", output_file)

def main():
    # Путь к папке с текстовыми файлами
    folder_path = 'путь_к_папке'

    # Имя выходного файла
    output_file = 'результат.txt'

    # Файлы для шапки, разделителя и конца
    header_file = 'шапка.txt'
    separator_file = 'разделитель.txt'
    footer_file = 'конец.txt'

    # Получение списка файлов в папке
    file_list = os.listdir(folder_path)

    # Поиск и сохранение текстовых значений из каждого файла
    results = []
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            file_results = search_text(file_path)
            results.extend(file_results)

    # Сохранение результатов в файл
    save_to_file(results, output_file, header_file, separator_file, footer_file)

if __name__ == '__main__':
    main()