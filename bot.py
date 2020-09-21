import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id


from dora_client import Dora_client

def write_msg(user_id, message):
    vk.method('messages.send', {
        'keyboard': keyboard.get_keyboard(),
        'user_id': user_id,
        'message': message,
        'random_id': get_random_id()})


token = "0b7170f5e40cecea90666360bda44e8a528b341e4c85042a0ce7ea013aef036fba8468021e17b906407d8"

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)

keyboard = VkKeyboard(one_time=True)
keyboard.add_button('R-', color=VkKeyboardColor.NEGATIVE)
keyboard.add_button('R+', color=VkKeyboardColor.POSITIVE)

bot = Dora_client()
bot.key = 'lvklvsdN'
last_message = {}
rating_stop = {}

print('Dora VK was started')
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.peer_id != event.user_id:
            answer = 'ping'
            write_msg(event.peer_id, answer)

        elif event.to_me:
            text = event.text
            lowtext = text.lower()

            if lowtext.startswith('add'):
                try:
                    arg1, arg2 = text.replace('add', '').split('=')
                    author = f'vk {event.user_id}'
                    response = bot.learn(arg1, arg2, author)
                    print(event.user_id, response)
                    answer = response['answer']

                except IndexError:
                    answer = 'Ошибочная команда. попробуй "add вопрос = ответ"'

            elif lowtext.startswith('r+') or lowtext.startswith('r-'):
                if rating_stop[event.user_id] == last_message[event.peer_id]:
                    answer = 'Больше одного раза голосовать нельзя.'

                else:
                    if lowtext.startswith('r+'): operator = 'rup'
                    if lowtext.startswith('r-'): operator = 'rdown'
                    response = bot.rating(operator, last_message[event.peer_id])
                    answer = response['answer']
                    rating_stop[event.user_id] = last_message[event.peer_id]
                    print(event.user_id, response)



            else:
                response = bot.answer(text)
                last_message[event.peer_id] = response['response_id']
                rating_stop[event.user_id] = -1
                answer = f"{response['answer']} ({response['coefficient']})"
                print(event.user_id, response)


            write_msg(event.peer_id, answer)

            # if request == "привет":
            #     write_msg(event.user_id, "Хай")
            # elif request == "пока":
            #     write_msg(event.user_id, "Пока((")
            # else:
            #     write_msg(event.user_id, "Не поняла вашего ответа...")