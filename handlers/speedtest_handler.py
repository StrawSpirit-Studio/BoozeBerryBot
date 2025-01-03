import speedtest

# Хендлер для тесту швидкості
async def speedtest_handler(client, message):
    # Виведення повідомлення про початок тесту
    await message.edit_text("🔄 **Починаю тестування швидкості з'єднання...**\nБудь ласка, зачекайте... ⏳")
    try:
        # Ініціалізація об'єкта для тестування швидкості
        st = speedtest.Speedtest()

        # Вибір найближчого сервера
        st.get_best_server()

        # Отримуємо швидкість завантаження та відвантаження в мегабітах за секунду
        download_speed = st.download() / 1_000_000  # Перетворюємо з біт/с в Мбіт/с
        upload_speed = st.upload() / 1_000_000  # Перетворюємо з біт/с в Мбіт/с
        
        # Отримуємо затримку (ping)
        ping = st.results.ping

        # Виведення результатів
        result_message = (
            f"📊 **Результати тесту швидкості:**\n"
            f"🔽 **Завантаження**: {download_speed:.2f} Mbps\n"
            f"🔼 **Відвантаження**: {upload_speed:.2f} Mbps\n"
            f"⏱️ **Затримка (ping)**: {ping} ms\n"
            f"🌐 **Тест проведений до сервера: {st.results.server['host']}**"
        )
        await message.edit_text(result_message)

    except Exception as e:
        await message.edit_text(f"⚠️ **Сталася помилка при тестуванні швидкості:** {str(e)}")
