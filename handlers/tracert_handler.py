from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import sr1
import asyncio

# Хендлер для traceroute
async def tracert_handler(client, message):
    if message.text and "$tracert" in message.text:
        command = message.text.split()

        # Якщо нема адреси
        if len(command) < 2:
            await message.reply("Використання: `$tracert <адреса>`\nНаприклад: `$tracert google.com`")
            return

        target = command[1]
        max_hops = 30
        timeout = 2
        traceroute_results = []

        await message.reply(f"🔍 Виконую tracer до {target}...")

        try:
            for ttl in range(1, max_hops + 1):
                pkt = IP(dst=target, ttl=ttl) / ICMP()
                reply = sr1(pkt, verbose=0, timeout=timeout)

                if reply is None:
                    traceroute_results.append(f"{ttl}: * Timeout")
                else:
                    traceroute_results.append(f"{ttl}: {reply.src}")
                    if reply.type == 0:  # Ехо-відповідь (мета досягнута)
                        break

                await asyncio.sleep(0.1)  # Додаємо паузу для зменшення навантаження

            result_message = f"🔗 **Tracert до {target}:**\n\n" + "\n".join(traceroute_results)
            await message.reply(result_message)

        except Exception as e:
            await message.reply(f"⚠️ Сталася помилка: {str(e)}")