import platform
import os
import ctypes
import subprocess
import asyncio
import pyautogui
from datetime import datetime
import win32gui
import win32process
import psutil

async def remote_handler(client, message):
    if message.text and "$lock" in message.text:
        try:
            if platform.system() == "Windows":
                ctypes.windll.user32.LockWorkStation()
                await message.edit_text("🔒 Комп'ютер заблоковано")
            elif platform.system() == "Linux":
                os.system("xdg-screensaver lock")
                await message.edit_text("🔒 Комп'ютер заблоковано")
            else:
                await message.edit_text("❌ Операційна система не підтримується")
        except Exception as e:
            await message.edit_text(f"❌ Помилка при блокуванні: {str(e)}")
            
    elif message.text and "$sleep" in message.text:
        try:
            if platform.system() == "Windows":
                await message.edit_text("😴 Переходжу в режим сну...")
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            elif platform.system() == "Linux":
                await message.edit_text("😴 Переходжу в режим сну...")
                os.system("systemctl suspend")
            else:
                await message.edit_text("❌ Операційна система не підтримується")
        except Exception as e:
            await message.edit_text(f"❌ Помилка при переході в режим сну: {str(e)}")
            
    elif message.text and "$spotify" in message.text:
        try:
            if platform.system() == "Windows":
                # Запускаємо Spotify
                spotify_path = os.path.expandvars(r"%APPDATA%\Spotify\Spotify.exe")
                if os.path.exists(spotify_path):
                    subprocess.Popen(spotify_path)
                    # Чекаємо поки Spotify запуститься
                    await asyncio.sleep(3)
                    # Симулюємо натискання Ctrl+L для переходу до бібліотеки
                    pyautogui.hotkey('ctrl', 'l')
                    await asyncio.sleep(1)
                    # Натискаємо пробіл для початку відтворення
                    pyautogui.press('space')
                    await message.edit_text("🎵 Spotify запущено, музика відтворюється")
                else:
                    await message.edit_text("❌ Spotify не знайдено")
            else:
                await message.edit_text("❌ Команда доступна тільки для Windows")
        except Exception as e:
            await message.edit_text(f"❌ Помилка при запуску Spotify: {str(e)}")
            
    elif message.text and "$hibernate" in message.text:
        try:
            if platform.system() == "Windows":
                await message.edit_text("💤 Переходжу в режим гібернації...")
                os.system("shutdown /h /f")
            elif platform.system() == "Linux":
                await message.edit_text("💤 Переходжу в режим гібернації...")
                os.system("systemctl hibernate")
            else:
                await message.edit_text("❌ Операційна система не підтримується")
        except Exception as e:
            await message.edit_text(f"❌ Помилка при гібернації: {str(e)}")
            
    elif message.text and "$screen" in message.text:
        try:
            msg =await message.reply("📸")
            
            # Отримуємо інформацію про активне вікно та його процес
            active_window = "Невідомо"
            window_time = "Невідомо"
            if platform.system() == "Windows":
                # Отримуємо хендл активного вікна
                hwnd = win32gui.GetForegroundWindow()
                active_window = win32gui.GetWindowText(hwnd)
                
                # Отримуємо PID процесу
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                try:
                    # Отримуємо інформацію про процес
                    process = psutil.Process(pid)
                    # Отримуємо час створення процесу
                    process_time = datetime.now() - datetime.fromtimestamp(process.create_time())
                    hours = process_time.seconds // 3600
                    minutes = (process_time.seconds % 3600) // 60
                    window_time = f"{hours}г {minutes}хв"
                except:
                    window_time = "Невідомо"
            
            # Створюємо папку downloads якщо її немає
            downloads_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downloads')
            os.makedirs(downloads_path, exist_ok=True)
            
            # Створюємо скріншот
            screenshot = pyautogui.screenshot()
            
            # Зберігаємо з унікальним ім'ям в downloads
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(downloads_path, filename)
            screenshot.save(filepath)
            
            # Формуємо текст повідомлення
            caption = (
                f"📸 **Скріншот робочого столу**\n"
                f"🪟 **Активне вікно**: {active_window}\n"
                f"⏱ **Час роботи**: {window_time}"
            )
            
            # Відправляємо файл з підписом
            await message.reply_photo(filepath, caption=caption)
            
            # Видаляємо тимчасовий файл
            os.remove(filepath)
            
            # Видаляємо повідомлення про процес
            await message.delete()
            await msg.delete()
            
        except Exception as e:
            await message.edit_text(f"❌ Помилка при створенні скріншоту: {str(e)}")