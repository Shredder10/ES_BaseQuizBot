from aiogram.utils.keyboard import InlineKeyboardBuilder
from db import get_quiz_index
from aiogram import types

quiz_data = [
    {
        'question': 'С кем из персонажей нельзя отправиться на поиски Шурика?',
        'options': ['Славя', 'Лена', 'Ульяна', 'Мику'],
        'correct_option': 3
    },
    {
        'question': 'Чьим соседом по домику является Женя?',
        'options': ['Славя', 'Не упоминалось', 'Мику', 'Лена'],
        'correct_option': 0
    },
    {
        'question': 'Какое из этих мест не входит в обходной лист?',
        'options': ['Библиотека', 'Музыкальный клуб', 'Столовая', 'Спортивный клуб'],
        'correct_option': 2
    },
    {
        'question': 'Кто дал Юле это имя?',
        'options': ['Её родители', 'Виола', 'Семён', 'Она сама'],
        'correct_option': 2
    },
    {
        'question': 'Почему Ольга Дмитриевна оставила Ульяну в лагере на время похода?',
        'options': ['За попытку подрыва статуи Генды', 'За постоянные проделки', 'За испорченный торт', 'Потому что Ульяна приболела'],
        'correct_option': 2
    },
    {
        'question': 'Кому посвящено дополнение "история одного пионера"?',
        'options': ['Семёну', 'Жене', 'Шурику', 'Ольге Дмитриевне'],
        'correct_option': 1
    },
    {
        'question': 'Кто из персонажей привёз Семёну тележку, когда он собирал ингридиенты для торта?',
        'options': ['Электроник', 'Ульяна', 'Славя', 'Лена'],
        'correct_option': 3
    },
    {
        'question': 'Кем Семёну пришлось один раз поработать в лагере?',
        'options': ['Завхозом', 'Медбратом', 'Тренером в спортклубе', 'Охранником'],
        'correct_option': 1
    },
    {
        'question': 'Как зовут Электроника в концовке Мику?',
        'options': ['Роутер', 'Серёжа', 'Электроник', 'Камера'],
        'correct_option': 0
    },
    {
        'question': 'Кто из персонажей является "лицом" "Бесконечного лета"?',
        'options': ['Алиса', 'Ольга Дмитриевна', 'Лена', 'Семён'],
        'correct_option': 2
    }
]

async def get_question(message, user_id):

    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()

    for option in range(len(answer_options)):
        builder.add(types.InlineKeyboardButton(
            text=answer_options[option],
            #callback_data="right_answer" if option == right_answer else "wrong_answer")
            callback_data=("1" + str(option)) if answer_options[option] == right_answer else ("0" + str(option)))
        )

    builder.adjust(1)
    return builder.as_markup()
