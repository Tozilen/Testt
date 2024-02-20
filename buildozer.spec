[app]

# Название вашего приложения
title = ToolChecker

# Имя пакета приложения
package.name = toolchecker

# Домен пакета (необходимо для упаковки под Android и iOS)
package.domain = org.example

# Версия приложения
version = 1.0

# Список расширений файлов, включая в сборку
source.include_exts = py,png,jpg,kv,atlas

# Требования к приложению
requirements = python3,kivy,plyer

# Разрешения Android
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Направление приложения (landscape, portrait или all)
orientation = portrait

# Полноэкранный режим (1 - полноэкранный, 0 - нет)
fullscreen = 1

# Каталог сборки
build_dir = bin

# Папка с исходными файлами (поменяйте 'src' на актуальное название вашей папки)
source.dir = tool checker