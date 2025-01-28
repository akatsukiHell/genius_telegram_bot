
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram import F, Router


import scrapy
from scrapy.crawler import CrawlerProcess


router = Router()

start_text = "Вы в главном меню.\nВыберите нужное действие."

from parse import albumData, SongDataSpider

process = CrawlerProcess()


# Кнопки для главного меню
def menu_reply_buttons():
    buttons = [
        [
        KeyboardButton(text="Копировать треклист"),
        KeyboardButton(text="Обложки"),
        KeyboardButton(text="Список релизов"),
        ]
    ]
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
    )
    
    return keyboard


# Кнопка назад
def back_button():

    buttons=[
        [
        KeyboardButton(text="Назад"),
        ]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
    )

    return keyboard


class Form(StatesGroup):
    menu = State()
    get_link_song = State()
    tracklist_markup = State()


# Команды
@router.message(CommandStart())
@router.message(F.text.casefold() == "назад")
async def command_start(message: Message, state: FSMContext) -> None:

    # Назначаем стейт главного меню
    await state.set_state(Form.menu)

    # Выводим сообщение пользователю
    await message.answer(
    text= start_text,
    reply_markup = menu_reply_buttons())



@router.message(Form.menu, F.text.casefold() == "копировать треклист")
async def get_tracklist_link(message: Message, state: FSMContext):

    await state.set_state(Form.get_link_song)

    await message.answer(
        "Пришлите ссылку на треклист:",
        reply_markup=back_button(),
    )


@router.message(Form.get_link_song)
async def tracklist_markup_link(message: Message, state: FSMContext) -> None:
    await state.update_data(get_link_song = message.text)

    if "genius.com/albums" in message.text:

        await message.answer(
            await message.text,
            
            #TODO: ^ реализовать получение ссылки на альбом от пользователя и передать её в parse.py для парсинга контента с возвратом результата
            
            await state.set_state(Form.tracklist_markup),
        )


        
    else:
        await message.answer(
            "Не удалось найти нужный альбом. Пришлите ссылку повторно."
        )



process.crawl(albumData, start_urls = [])
process.crawl(SongDataSpider, start_urls = ["https://genius.com/albums/Madk1d/He-said-lets-go"])
process.start()