from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

# from congif_reader import Settings
from fluent.runtime import FluentLocalization
from keyboards.inline_keyboard import menu_buttons


router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, l10n: FluentLocalization):
    await message.answer(l10n.format_value("start-text"), reply_markup=menu_buttons(l10n))



