from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from questions import quiz_data, get_question
from db import get_quiz_index, update_quiz_index, write_quiz_results

API_TOKEN = '7569088235:AAF0THCIRR0GagM5TvDbJk70YmqoF-m8UUQ'

user_answers = []

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.callback_query(F.data[0] == "1")
async def right_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    current_question_index = await get_quiz_index(callback.from_user.id)
    await callback.message.answer("Ваш ответ: " + quiz_data[current_question_index]['options'][int(callback.data[1])])
    user_answers.append(int(callback.data[1]))
    await callback.message.answer("Верно!")
    
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)


    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        #await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        await end_quiz(callback.message)


@dp.callback_query(F.data[0] == "0")
async def wrong_answer(callback: types.CallbackQuery):
    
    
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    
    current_question_index = await get_quiz_index(callback.from_user.id)
    user_answers.append(int(callback.data[1]))
    await callback.message.answer("Ваш ответ: " + quiz_data[current_question_index]['options'][int(callback.data[1])])
    correct_option = quiz_data[current_question_index]['correct_option']
    await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)
    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        #await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        await end_quiz(callback.message)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз по игре 'Бесконечное лето'! Все вопросы связаны лишь с официальной историей, представленной разработчиками.", reply_markup=builder.as_markup(resize_keyboard=True))


@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):

    await message.answer(f"Давайте начнем квиз!")
    await new_quiz(message)

async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index)
    await get_question(message, user_id)


async def end_quiz(message):
    await message.answer("Это был последний вопрос. Квиз завершен!")
    user_id = message.from_user.id
    await write_quiz_results(user_id, user_answers)

    result = "Ваша статистика:"

    corr = 0
    for answer in range(len(user_answers)):
        correct_option = quiz_data[answer]['correct_option']
        
        result = result + f"\n{answer + 1}. {user_answers[answer] + 1} ({quiz_data[answer]['options'][user_answers[answer]]})"
        if correct_option == user_answers[answer]:
            corr = corr + 1
        else:
            result = result + f"\n (правильный ответ - {quiz_data[answer]['options'][correct_option]})"
        result = result + ";"
    
    result = result + f"\n\nВсего правильных ответов: {corr}."

    await message.answer(result)
