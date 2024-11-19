# Этот файл нужен для открытия двух python файлов поочерёдно. сначала запускается flask сайт потом уже pyqt программа.
# Файл должен находиться в корневой папке для правильной работы, но в этом нету необходимости так как
# я преобразовал этот python файл в exe через pyinstaller.
import subprocess
import time

process1 = subprocess.Popen(['python', 'main.py'])

time.sleep(2)

process2 = subprocess.Popen(['python', 'src/pyqtweb.py'])