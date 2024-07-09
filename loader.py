# импорты ихихихихиха
import hashlib
import os
import subprocess
import zipfile
import requests

from colorama import Fore, init

init(autoreset=True)

# скачка
def download_file(url, local_filename):
    response = requests.get(url)
    with open(local_filename, 'wb') as f:
        f.write(response.content)
    print(f"{Fore.LIGHTWHITE_EX}Файл скачан: {local_filename}")

# получаем хэш файла чтобы сравнить на сервере и обновить если изменено лол кек
def get_file_hash(filename):
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# получаем хэш на сервере чтоб не втыкал
def get_server_file_hash(url):
    response = requests.get(url)
    sha256_hash = hashlib.sha256()
    sha256_hash.update(response.content)
    return sha256_hash.hexdigest()

# проверяем и обновляем клиент
def check_and_update_file(url, local_filename):
    if not os.path.exists(local_filename):
        print(f"{Fore.LIGHTWHITE_EX}Клиент не скачан, скачиваем...")
        download_file(url, local_filename)
        return

    local_file_hash = get_file_hash(local_filename)
    server_file_hash = get_server_file_hash(url)

    if local_file_hash != server_file_hash:
        print(f"{Fore.LIGHTWHITE_EX}Файл на сервере обновлён, обновляем!")
        download_file(url, local_filename)
    else:
        print(f"{Fore.LIGHTWHITE_EX}У вас последняя версия клиента.")

# экстрактим zip
def extract_zip_file(zip_file, extract_to, what):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"{Fore.LIGHTWHITE_EX}{what} распакована: {extract_to}")

# устанавливаем java corretto
def setup_java_corretto(url, download_path, install_path):
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    if not os.path.exists(install_path):
        os.makedirs(install_path)

    local_filename = os.path.join(download_path, "java17.zip")
    if not os.path.exists(local_filename):
        download_file(url, local_filename)
        extract_zip_file(local_filename, install_path, "Java")
        os.remove(local_filename)
        print(f"{Fore.LIGHTWHITE_EX}Временный файл {local_filename} был удалён.")

# запуск
def run(ram="2048", username="Cat"):
    ram = int(ram)
    command = [
        r"C:\Cat\jdk17.0.11_9\bin\javaw.exe",
        r" -jar C:\Cat\cat.jar"
        " -Xms{}M".format(ram),
        " -Djava.library.path=C:\\Cat\\natives",
        " -Xss2M",
        " --username",
        f" {username}",
        " --version",
        " 1.16.5",
        " --gameDir",
        " C:\\Cat",
        " --assetsDir",
        " C:\\Cat\\assets",
        " --assetIndex",
        " 1.16",
        " --uuid",
        " N/A",
        " --accessToken",
        " 0",
        " --userType",
        " legacy",
        " --versionType",
        " release",
        " --width",
        " 925",
        " --height",
        " 530",
    ]

    os.system(" ".join(command))

# никому не нужные переменные
url = "https://github.com/BrightCat14/catclient/releases/download/ex/cat.jar"
local_filename = "C:\\Cat\\cat.jar"
javaurl = "https://corretto.aws/downloads/latest/amazon-corretto-17-x64-windows-jdk.zip"
download_path = "C:\\Cat\\cache"
install_path = "C:\\Cat"


def main_menu():
    while True:
        choice = input(f"""
                            {Fore.CYAN} ██████  █████  ████████      ██████ ██      ██ ███████ ███    ██ ████████ 
                            {Fore.CYAN}██      ██   ██    ██        ██      ██      ██ ██      ████   ██    ██    
                            {Fore.CYAN}██      ███████    ██        ██      ██      ██ █████   ██ ██  ██    ██    
                            {Fore.CYAN}██      ██   ██    ██        ██      ██      ██ ██      ██  ██ ██    ██    
                            {Fore.CYAN} ██████ ██   ██    ██         ██████ ███████ ██ ███████ ██   ████    ██    
                                    {Fore.LIGHTWHITE_EX}1 - Запустить
                                    {Fore.LIGHTWHITE_EX}2 - Сменить ник (по умолчанию - Cat)
                                    {Fore.LIGHTWHITE_EX}3 - Изменить оперативную память (по умолчанию 2048 МБ)
        {Fore.LIGHTWHITE_EX}Выбор: """)

        username = "Cat"
        ram = "2048"

        if choice == '2':
            username = input(f"{Fore.LIGHTWHITE_EX}Введите ваш ник: ")
            if not username:
                username = "Cat"
            continue
        elif choice == '3':
            ram = input(f"{Fore.LIGHTWHITE_EX}Введите количество оперативной памяти (в МБ): ")
            if not ram:
                ram = "2048"
            continue
        elif choice == '1':
            print(f"{Fore.LIGHTWHITE_EX}Ждите пока клиент запустится")
            # делаем грязь
            check_and_update_file(url, local_filename)
            setup_java_corretto(javaurl, download_path, install_path)
            run(ram=ram, username=username)
            continue  # cсделали грязь



main_menu()
