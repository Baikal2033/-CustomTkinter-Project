import customtkinter as ctk
import winreg
import ctypes
import os
from PIL import Image
import winshell
from win32com.client import Dispatch
import psutil
import threading
import urllib.request
import time
import tempfile
import subprocess
import shutil

def handle_switch_choice():
    if var_switch.get():
        ctk.set_appearance_mode("light")
        label.configure(text_color="black")
        btn_1.configure(text_color="black", fg_color="orange")
        btn_2.configure(text_color="black", fg_color="orange")
        btn_3.configure(text_color="black", fg_color="orange")
        btn_4.configure(text_color="black", fg_color="orange")
        btn_5.configure(text_color="black", fg_color="orange")
        btn_6.configure(text_color="black", fg_color="orange")
        switch.configure(progress_color="orange")
    else:
        ctk.set_appearance_mode("dark")
        label.configure(text_color="white")
        btn_1.configure(text_color="white", fg_color="#26a15c")
        btn_2.configure(text_color="white", fg_color="#26a15c")
        btn_3.configure(text_color="white", fg_color="#26a15c")
        btn_4.configure(text_color="white", fg_color="#26a15c")
        btn_5.configure(text_color="white", fg_color="#26a15c")
        btn_6.configure(text_color="white", fg_color="#26a15c")
        switch.configure(fg_color="#434b4d")

def background():
    dialog_window = ctk.CTkToplevel()
    dialog_window.title("фон")
    dialog_window.geometry("500x300")


    def give_answer(lbl_nmb):

        if lbl_nmb == 1:
            image_path = os.path.join(os.path.dirname(__file__), "images", "forest.jpg")
        elif lbl_nmb == 2:
            image_path = os.path.join(os.path.dirname(__file__), "images", "car.jpg")
        else:
            image_path = os.path.join(os.path.dirname(__file__), "images", "lake.jpg")

        if not os.path.exists(image_path):
            print(f"Ошибка: файл не найден - {image_path}")
            return False

        try:
            # Открываем раздел реестра для обоев
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Control Panel\Desktop",
                0,
                winreg.KEY_SET_VALUE
            )

            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "10")
            winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0")
            winreg.CloseKey(key)

            ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
            dialog_window.destroy()
            return True
        except Exception as e:
            print(f"Ошибка при смене обоев: {e}")
            return False

    lbl_question = ctk.CTkLabel(master=dialog_window, text="Какой фон установить?", font=my_font)

    lbl_1 = ctk.CTkLabel(master=dialog_window)
    lbl_1.configure(text="", image=image_ctk_utility_1)
    lbl_1.bind("<Button-1>", lambda e: give_answer(lbl_nmb=1))
    lbl_1.configure(cursor="hand2")

    lbl_2 = ctk.CTkLabel(master=dialog_window)
    lbl_2.configure(text="", image=image_ctk_utility_2)
    lbl_2.bind("<Button-1>",lambda e: give_answer(lbl_nmb=2))
    lbl_2.configure(cursor="hand2")

    lbl_3 = ctk.CTkLabel(master=dialog_window)
    lbl_3.configure(text="", image=image_ctk_utility_3)
    lbl_3.bind("<Button-1>",lambda e: give_answer(lbl_nmb=3))
    lbl_3.configure(cursor="hand2")


    rows, columns = 2, 3
    for i in range(rows):
        if i == 1:
            dialog_window.rowconfigure(index=i, weight=3)
        else:
            dialog_window.rowconfigure(index=i, weight=1)
    for i in range(columns):
        dialog_window.columnconfigure(index=i, weight=1)
    lbl_question.grid(row=0, column=0, columnspan=3)
    lbl_1.grid(row=1, column=0)
    lbl_2.grid(row=1, column=1)
    lbl_3.grid(row=1, column=2)

def basket():
    basket_window = ctk.CTkToplevel()
    basket_window.title("мусор")
    basket_window.geometry("300x200")

    def give_yes():
        try:
            winshell.recycle_bin().empty(
                confirm=False,
                show_progress=False,
                sound=False
            )
            basket_window.destroy()
        except Exception as e:
            basket_window.destroy()
            return f"Ошибка: {e}"

    def give_no():
        basket_window.destroy()

    lbl_question = ctk.CTkLabel(master=basket_window, text="Очистить корзину?", font=my_font)
    btn_yes = ctk.CTkButton(master=basket_window, font=my_font, text="Да", width=60, command=give_yes, fg_color="#26a15c")
    btn_no = ctk.CTkButton(master=basket_window, font=my_font, text="Нет", width=60, command=give_no, fg_color="#26a15c")

    rows, columns = 2, 2
    for i in range(rows):
        basket_window.rowconfigure(index=i, weight=1)
    for i in range(columns):
        basket_window.columnconfigure(index=i, weight=1)
    lbl_question.grid(row=0, column=0, columnspan=2)
    btn_yes.grid(row=1, column=0)
    btn_no.grid(row=1, column=1)

def temperature():
    temperature_window = ctk.CTkToplevel()
    temperature_window.title("цп")
    temperature_window.geometry("300x200")
    textbox = ctk.CTkTextbox(master=temperature_window)
    textbox.configure(font=my_font, height=180, width=280)

    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    info = (
        f"CPU: {cpu}%\n"
        f"RAM: {ram.percent}%\n"
        f"Диск C: {disk.percent}% занято"
    )

    textbox.insert(0.0, info)

    rows, columns = 1, 1
    for i in range(rows):
        temperature_window.rowconfigure(index=i, weight=1)
    for i in range(columns):
        temperature_window.columnconfigure(index=i, weight=1)
    textbox.grid(row=0, column=0)


def internet():
    internet_window = ctk.CTkToplevel()
    internet_window.title("сеть")
    internet_window.geometry("400x300")

    textbox = ctk.CTkTextbox(master=internet_window)
    textbox.configure(font=my_font, height=100)

    label = ctk.CTkLabel(master=internet_window)
    label.configure(
        text="Запуск теста интернета...",
        font=my_font,
        text_color="white"
    )

    def test_internet(output_widget, status_label):
        status_label.configure(text="Тест запущен... Ждите!")

        def run():
            try:
                test_urls = [
                    ("https://speed.hetzner.de/100MB.bin", 100),  # 100 МБ
                    ("http://testfiles.org/10MB.zip", 10),  # 10 МБ (запасной)
                ]

                download_speed = 0

                for url, size_mb in test_urls:
                    try:
                        status_label.configure(text=f"Загрузка тестового файла {size_mb} МБ...")

                        start_time = time.time()

                        # Скачиваем файл
                        response = urllib.request.urlopen(url, timeout=30)
                        data = response.read()

                        elapsed = time.time() - start_time

                        if elapsed > 0:
                            speed_mbps = (size_mb * 8) / elapsed
                            download_speed = speed_mbps

                            result_text = (
                                f"Скорость: {download_speed:.1f} Мбит/с\n"
                                f"Размер файла: {size_mb} МБ\n"
                                f"Время: {elapsed:.1f} сек\n"
                                f"Сервер: Hetzner (Германия)"
                            )
                            break

                    except Exception:
                        continue

                if download_speed == 0:
                    raise Exception("Не удалось подключиться к тестовым серверам")

                output_widget.delete("0.0", "end")
                output_widget.insert("0.0", result_text)
                status_label.configure(text="Тест завершён!")

            except Exception as e:
                error_msg = f"Ошибка: {e}"
                output_widget.delete("0.0", "end")
                output_widget.insert("0.0", error_msg)
                status_label.configure(text="Нет интернета или сервер недоступен")

        thread = threading.Thread(target=run, daemon=True)
        thread.start()

    test_internet(textbox, label)

    rows, columns = 2, 1
    for i in range(rows):
        if i == 1:
            internet_window.rowconfigure(index=i, weight=3)
        else:
            internet_window.rowconfigure(index=i, weight=1)
    for i in range(columns):
        internet_window.columnconfigure(index=i, weight=1)

    label.grid(row=0, column=0)
    textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

def time():
    time_window = ctk.CTkToplevel()
    time_window.title("таймер")
    time_window.geometry("500x200")

    def shutdown_in():
        subprocess.run("shutdown /a", shell=True)
        minutes = int(entry.get())
        seconds = minutes * 60
        subprocess.run(f"shutdown /s /t {seconds}", shell=True)
        lbl.configure(text=f"ПК выключиться через {minutes} минут")

    def cancel_shutdown():
        subprocess.run("shutdown /a", shell=True)
        lbl.configure(text=f"Отключение ПК отменено")

    lbl = ctk.CTkLabel(master=time_window, text="Через сколько минут выключить ПК?", font=my_font)
    entry = ctk.CTkEntry(master=time_window, font=my_font, width=300, placeholder_text="Введите ответ")
    btn_1 = ctk.CTkButton(master=time_window, font=my_font, text="Ответить", width=100,
                        command=shutdown_in, fg_color="#26a15c")
    btn_2 = ctk.CTkButton(master=time_window, font=my_font, text="Отменить", width=100,
                          command=cancel_shutdown, fg_color="#26a15c")

    rows, columns = 4, 1
    for i in range(rows):
        time_window.rowconfigure(index=i, weight=1)
    for i in range(columns):
        time_window.columnconfigure(index=i, weight=1)
    lbl.grid(row=0, column=0)
    entry.grid(row=1, column=0)
    btn_1.grid(row=2, column=0)
    btn_2.grid(row=3, column=0)

def cache():
    cache_window = ctk.CTkToplevel()
    cache_window.title("кеш")
    cache_window.geometry("300x200")

    def give_yes():
        results = []

        try:
            subprocess.Popen('cleanmgr.exe')
            results.append("Запущена очистка диска Windows")
        except Exception as e:
            results.append(f"Очистка диска: {e}")

        deleted_count = 0
        temp_dirs = [
            tempfile.gettempdir(),
            r"C:\Windows\Temp"
        ]

        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            os.remove(file_path)
                            deleted_count += 1
                        except (PermissionError, OSError):
                            pass

        results.append(f"Удалено {deleted_count} временных файлов")

        chrome_cache_path = os.path.expanduser(
            r'~\AppData\Local\Google\Chrome\User Data\Default\Cache'
        )

        if os.path.exists(chrome_cache_path):
            try:
                shutil.rmtree(chrome_cache_path)
                results.append("Кеш Chrome очищен")
            except Exception as e:
                results.append(f"Кеш Chrome: {e}")
        else:
            results.append("ℹКеш Chrome не найден")

        return "\n".join(results)

    def give_no():
        cache_window.destroy()

    lbl_question = ctk.CTkLabel(master=cache_window, text="Очистить кеш?", font=my_font)
    btn_yes = ctk.CTkButton(master=cache_window, font=my_font, text="Да", width=60, command=give_yes,
                            fg_color="#26a15c")
    btn_no = ctk.CTkButton(master=cache_window, font=my_font, text="Нет", width=60, command=give_no,
                           fg_color="#26a15c")

    rows, columns = 2, 2
    for i in range(rows):
        cache_window.rowconfigure(index=i, weight=1)
    for i in range(columns):
        cache_window.columnconfigure(index=i, weight=1)
    lbl_question.grid(row=0, column=0, columnspan=2)
    btn_yes.grid(row=1, column=0)
    btn_no.grid(row=1, column=1)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("Панель управления")
root.geometry("600x400")
my_font = ctk.CTkFont(family="Roboto", size=25)

image_object_1 = Image.open("images/forest.jpg")
image_ctk_utility_1 = ctk.CTkImage(dark_image=image_object_1, size=(150, 150))
image_object_2 = Image.open("images/car.jpg")
image_ctk_utility_2 = ctk.CTkImage(dark_image=image_object_2, size=(150, 150))
image_object_3 = Image.open("images/lake.jpg")
image_ctk_utility_3 = ctk.CTkImage(dark_image=image_object_3, size=(150, 150))

rows, columns = 4, 3
for i in range(rows):
    root.rowconfigure(index=i, weight=1)
for i in range(columns):
    root.columnconfigure(index=i, weight=1)

label = ctk.CTkLabel(master=root)
label.configure(
    text="Панель управления",
    font=my_font,
    text_color="white"

)

btn_1 = ctk.CTkButton(master=root)
btn_1.configure(text=f"фон", font=my_font, width=100, height=25, command=background, fg_color="#26a15c")

btn_2 = ctk.CTkButton(master=root)
btn_2.configure(text=f"мусор", font=my_font, width=100, height=25, command=basket, fg_color="#26a15c")

btn_3 = ctk.CTkButton(master=root)
btn_3.configure(text=f"цп", font=my_font, width=100, height=25, command=temperature, fg_color="#26a15c")

btn_4 = ctk.CTkButton(master=root)
btn_4.configure(text=f"сеть", font=my_font, width=100, height=25, command=internet, fg_color="#26a15c")

btn_5 = ctk.CTkButton(master=root)
btn_5.configure(text=f"таймер", font=my_font, width=100, height=25, command=time, fg_color="#26a15c")

btn_6 = ctk.CTkButton(master=root)
btn_6.configure(text=f"кеш", font=my_font, width=100, height=25, command=cache, fg_color="#26a15c")

var_switch = ctk.BooleanVar()
switch = ctk.CTkSwitch(master=root, variable=var_switch, onvalue=True, offvalue=False)
switch.configure(text="Тема", font=my_font, fg_color="#434b4d")
switch.configure(command=handle_switch_choice)
var_switch.set(False)

label.grid(row=0, column=0, columnspan=3)
btn_1.grid(row=1, column=0)
btn_2.grid(row=1, column=1)
btn_3.grid(row=1, column=2)
btn_4.grid(row=2, column=0)
btn_5.grid(row=2, column=1)
btn_6.grid(row=2, column=2)
switch.grid(row=3, column=2)

root.mainloop()
