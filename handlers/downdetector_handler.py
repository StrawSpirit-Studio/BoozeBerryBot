import requests
from config import DOWDETECTOR_API_URL  # Додайте URL API Downdetector у ваш config.py
import logging

logger = logging.getLogger("downdetector")

async def downdetector_handler(client, message):
    try:
        # Перевірка команди
        if message.text and "$downdetector" in message.text:
            command_parts = message.text.split()
            if len(command_parts) < 2:
                await message.edit_text("🛑 Використовуйте команду $downdetector [назва_сторінки]")
                return
            
            page_name = command_parts[1]
            await message.edit_text(f"🔄 Перевірка статусу для {page_name}...")

            # Запит до API Downdetector
            response = requests.get(f"{DOWDETECTOR_API_URL}/{page_name}")
            if response.status_code == 200:
                data = response.json()
                status = data.get("status", "Невідомий статус")
                await message.edit_text(f"🎯 Статус {page_name}: {status}")
            else:
                await message.edit_text("❌ Помилка при отриманні даних. Спробуйте ще раз.")
                logger.error(f"Помилка запиту до Downdetector: {response.status_code}")

    except Exception as e:
        error_text = f"❌ Помилка: {str(e)}"
        await message.edit_text(error_text)
        logger.error(f"Помилка Downdetector: {e}", exc_info=True) 