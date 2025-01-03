from ping3 import ping

# Хендлер для пінгування серверів чи сайтів
async def sping_handler(client, message):
    if message.text and "$sping" in message.text:
        # Перевірка на наявність аргументів
        command = message.text.split()
        
        # Якщо аргументів немає, виводимо підказку
        if len(command) < 2:
            await message.edit_text("🔍 **Використання:**\n`$sping <адреса> [кількість] [байти]`\n📍 Наприклад: `$sping google.com 10 64` або `$sping 192.168.0.1`\n📌 **Кількість пінгів** за замовчуванням = 4, **розмір пакету** за замовчуванням = 32 байти.")
            return

        host = command[1]
        num_pings = 4  # Кількість пінгів за замовчуванням
        packet_size = 32  # Розмір пакету в байтах за замовчуванням

        # Якщо є додаткові аргументи, змінюємо кількість пінгів і байти
        if len(command) >= 3:
            try:
                num_pings = int(command[2])
            except ValueError:
                await message.edit_text("❌ **Помилка:** Кількість пінгів повинна бути числом.")
                return

        if len(command) >= 4:
            try:
                packet_size = int(command[3])
            except ValueError:
                await message.edit_text("❌ **Помилка:** Розмір пакету (байти) повинен бути числом.")
                return

        response_times = []

        try:
            # Пінгуємо хост кілька разів
            for _ in range(num_pings):
                response_time = ping(host, size=packet_size)
                if response_time is not None:
                    response_times.append(response_time * 1000)  # Перетворюємо в мс
                else:
                    response_times.append(None)

            # Якщо є пінги
            if response_times:
                successful_pings = [time for time in response_times if time is not None]
                failed_pings = num_pings - len(successful_pings)
                
                if successful_pings:
                    min_time = min(successful_pings)
                    max_time = max(successful_pings)
                    avg_time = sum(successful_pings) / len(successful_pings)

                    result_message = f"🌐 **Pinging {host} with {packet_size} bytes of data:**\n"
                    for i, time in enumerate(response_times):
                        if time is not None:
                            result_message += f"✅ **Reply** from {host}: bytes={packet_size} time={time:.0f}ms TTL=64\n"
                        else:
                            result_message += f"❌ **Request timed out.**\n"
                    
                    result_message += f"\n📊 **Ping statistics** for {host}:\n"
                    result_message += f"    📤 Sent = {num_pings}, 📥 Received = {len(successful_pings)}, ❌ Lost = {failed_pings} ({(failed_pings / num_pings) * 100}% loss)\n"
                    result_message += f"⏳ Approximate round trip times in milli-seconds:\n"
                    result_message += f"    🕒 Minimum = {min_time:.0f}ms, 🕔 Maximum = {max_time:.0f}ms, 🕐 Average = {avg_time:.0f}ms"
                    
                    await message.edit_text(result_message)
                else:
                    await message.edit_text(f"❌ Не вдалося отримати відповідь від {host} після {num_pings} пінгів.")
            else:
                await message.edit_text(f"❌ Не вдалося пінгувати {host}.")
                
        except Exception as e:
            await message.edit_text(f"⚠️ **Сталася помилка:** {str(e)}")
