import random

RESPONSES = {
    'positive': [
        "Так, без сумніву. ✅",
        "Так, це очевидно. 👍",
        "Без сумніву. ✔️",
        "Без сумніву, так. 🙌",
        "Так, це виглядає вірно. 💯"
    ],
    'neutral': [
        "Можливо. 🤔",
        "Може бути. 🤷‍♂️",
        "Питання занадто складне. 🧐",
        "Я не можу сказати зараз. ❓",
        "Залиште це на потім. ⏳"
    ],
    'negative': [
        "Ні, це не станеться. ❌",
        "Без шансів. 🚫",
        "Ні, не чекай цього. 🚫",
        "Це не відбудеться. 😔",
        "Скоріше за все, ні. 😕"
    ]
}

async def eight_ball_handler(client, message):
    command = message.text.split()

    if len(command) < 2:
        await message.reply(
            "🎱 **Використання:** `$8ball <питання>`\n"
            "**Приклад:** `$8ball Чи буде завтра дощ?`"
        )
        return

    question = ' '.join(command[1:])
    
    response_type = random.choice(['positive', 'neutral', 'negative'])
    response = random.choice(RESPONSES[response_type])
    
    await message.reply(
        f"🎱 **Питання:** {question}\n"
        f"**Магічна куля каже:** {response}"
    )
