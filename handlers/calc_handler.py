from sympy import symbols, simplify, Eq, solve
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application


# Налаштування трансформацій
transformations = (standard_transformations + (implicit_multiplication_application,))

async def calc_handler(client, message):
    expression = message.text[len("$calc "):].strip()
    x = symbols('x')  # Стандартна змінна для рівнянь

    try:
        steps = []
        # Перевіряємо, чи є матриця в виразі
        if "Matrix" in expression:
            steps.append(f"Вираз: `{expression}`")
            
            # Обробка матриць
            parsed_expression = parse_expr(expression, transformations=transformations)
            steps.append(f"Перетворюємо у символьний формат: `{parsed_expression}`")
            
            # Спрощуємо вираз
            result = simplify(parsed_expression)
            steps.append(f"Спрощуємо вираз: `{result}`")
            
            explanation = "\n".join(steps)
            await message.reply_text(f"**Кроки:**\n{explanation}\n\n**Результат:** `{result}`")
        
        # Якщо є знак рівності, обробляємо як рівняння
        elif '=' in expression:
            left, right = expression.split('=')
            steps.append(f"Рівняння: `{left} = {right}`")
    
            # Формуємо рівняння
            left_expr = parse_expr(left, transformations=transformations)
            right_expr = parse_expr(right, transformations=transformations)
            equation = Eq(left_expr, right_expr)
            steps.append(f"Перетворюємо на символьне рівняння: `{equation}`")

            # Розв'язуємо рівняння
            solutions = solve(equation, x)
            steps.append(f"Розв'язуємо рівняння: `{solutions}`")

            explanation = "\n".join(steps)
            await message.reply_text(f"**Кроки:**\n{explanation}\n\n**Результат:** `x = {solutions}`")

        else:
            # Це математичний вираз
            steps.append(f"Вираз: `{expression}`")

            # Символьний розбір виразу
            parsed_expression = parse_expr(expression, transformations=transformations)
            steps.append(f"Перетворюємо у символьний формат: `{parsed_expression}`")

            # Спрощуємо вираз
            result = simplify(parsed_expression)
            steps.append(f"Спрощуємо вираз: `{result}`")

            explanation = "\n".join(steps)
            await message.reply_text(f"**Кроки:**\n{explanation}\n\n**Результат:** `{result}`")

    except Exception as e:
        await message.reply_text(f"⚠️ Помилка: не вдалося обчислити вираз.\n{str(e)}")
