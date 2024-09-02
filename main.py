import vk_api  #основная библиотека для работы с вк апи
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import requests
import random



# для взаимодейсвтия бота нам необходим токен группы, от имени которой будет работать бот
GROUP_TOKEN = '' напишите сюла токен, полученный в группе ВК
GROUP_ID = '' напишите сюда id вашей группы ВК


#так как у нас бот отвечает за погоду, был выбран open source сервис для прогнозов погоды
KEY_WORDS = ['погода']
WEATHER_API_KEY = ''  # напишите сюда токен полученный в сервисе прогноза погоды
DEFAULT_CITY = 'Nizhniy Novgorod'



#основная функция для запроса погоды в нужном городе

def get_weather(city):
    api_url = f"http://api.weatherstack.com/current?access_key={WEATHER_API_KEY}&query={city}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        if 'current' in data:
            weather_data = data['current']
            temperature = weather_data['temperature']
            weather_description = weather_data['weather_descriptions'][0]
            humidity = weather_data['humidity']

            weather_message = (
                f"Погода в городе {city}:\n"
                f"Температура: {temperature}°C\n"
                f"Влажность: {humidity}%"
            )
            return weather_message
        else:
            return "Ошибка получения данных о погоде."
    else:
        return "Ошибка запроса к сервису погоды."



#основная функция бота
def main():
    vk_session = vk_api.VkApi(token=GROUP_TOKEN)
    longpoll = VkBotLongPoll(vk_session, GROUP_ID)
    vk = vk_session.get_api()

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.object.message
            message_text = message['text'].lower()
            peer_id = message['peer_id']

            for keyword in KEY_WORDS:
                if keyword in message_text:
                    try:
                        weather_message = get_weather(DEFAULT_CITY)  # Можно добавить обработку города из сообщения
                        vk.messages.send(
                            peer_id=peer_id,
                            message=weather_message,
                            random_id=random.randint(1, 2 ** 32)
                        )
                    except vk_api.exceptions.ApiError as e:
                        print(f"Ошибка API VK: {e}")


if __name__ == '__main__':
    main()
