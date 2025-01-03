# Версія додатку
app_version = '1.0.0' # Версія бота

# Telegram API налаштування
API_ID = "" # ID API для Telegram
API_HASH = "" # Hash API для Telegram
PHONE_NUMBER = "" # Номер телефону для авторизації в Telegram

# Префікси для команд
PREFIXES = "$"

# Шляхи до моделей та бінарних файлів
FFMPEG_PATH = "packages/ffmpeg/bin/ffmpeg.exe" # Шлях до бінарного файлу FFMPEG (НЕ МОЖЕТ БУТИ ЗМІНЕНИЙ)

THE_CAT_API_KEY = "" # Ключ для доступу до сервісу The Cat API

# Налаштування Whisper для STT
whisper_presets = 'accurate' # Підтримується: accurate, fast, normal, custom
beam_size = 10 # Використовується для керування кількістю варіантів, які Whisper буде розглядати    
best_of = 10 # Використовується для керування кількістю варіантів, які Whisper буде розглядати
temperature = 0.2 # Використовується для керування випадковістю результату