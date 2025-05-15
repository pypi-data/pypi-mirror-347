from openai import OpenAI

def zap(text, api_key="64ef86312b5b4226a2eced79eb640b79"):
    """
    Отправляет запрос к ИИ и возвращает ответ.
    
    Args:
        text (str): Текст запроса
        api_key (str): API ключ для доступа к сервису
        
    Returns:
        str: Ответ от ИИ
    """
    client = OpenAI(
        base_url="https://api.aimlapi.com/v1",
        api_key=api_key,
    )

    response = client.chat.completions.create(
        model="Qwen/Qwen3-235B-A22B-fp8-tput",
        messages=[
            {
                "role": "system",
                "content": "Ты - помощник, который даёт чёткие и точные ответы. Не показывай процесс размышления, сразу давай правильный ответ. Если это математическая задача, покажи формулу и вычисления. Если это вопрос по программированию, давай готовый код. Если это общий вопрос, давай краткий и информативный ответ."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.3,
        top_p=0.8,
        frequency_penalty=0.5,
        max_tokens=4096,
    )

    return response.choices[0].message.content 