from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from  aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import get_all_products, is_included, add_user
product_sq = get_all_products()


api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Информация')
            ],
            [
            KeyboardButton(text='Купить'),
            KeyboardButton(text='Регистрация')
             ],

    ], resize_keyboard=True
)

in_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text= 'Рассчитать норму калорий', callback_data = 'calories'),
            InlineKeyboardButton(text= 'Формула расчёта', callback_data='formula')
        ]
    ]
)

buy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Product1", callback_data="product_buying'),
            InlineKeyboardButton(text='Product2", callback_data="product_buying'),
            InlineKeyboardButton(text='Product3", callback_data="product_buying'),
            InlineKeyboardButton(text='Product4", callback_data="product_buying')
        ]
    ]
)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

@dp.message_handler(text = 'Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()

@dp.message_handler(state = RegistrationState.username)
async def set_username(message, state):
    if not is_included(message.text):
        await message.answer('Пользователь существует, введите другое имя')
    else:
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()

@dp.message_handler(state = RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email = message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()

@dp.message_handler(state = RegistrationState.age)
async def set_age(message, state):
    data = await state.get_data()
    username = data.get('username')
    email = data.get('email')
    age = message.text
    add_user(username, email, age)
    await message.answer('Регистрация прошла успешно!')
    await state.finish()

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = in_kb)

@dp.callback_query_handler(text = 'formula')
async def get_formula(call):
    await call.message.answer('(10 х вес в кг) + (6,25 х рост в см) – (5 х возраст в г) + 5')
    await call.answer()

@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(text=['Рассчитать'])
async def set_age(message):
    await message.answer('Введите свой возраст')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    norma = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'Ваша норма каллорий: {norma}')
    await state.finish()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for k in product_sq:
        with open(f'{k[0]}.png', 'rb') as img:
            await message.answer_photo(img, f"Название: {k[1]} | Описание: {k[2]} | Цена: {k[3]}")
    await message.answer('Выберите продукт для покупки:', reply_markup=buy_kb)

@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
