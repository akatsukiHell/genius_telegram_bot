from functools import cache

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fluent.runtime import FluentLocalization
from aiogram.types import Message

@cache
def menu_buttons(l10n: FluentLocalization):
    keyboard = [
        [InlineKeyboardButton(text=l10n.format_value('tracklist-button'), callback_data="tracklist_markup")],
        [InlineKeyboardButton(text = l10n.format_value('change_lang'), callback_data='change_to_eng')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

@cache
def back_button(l10n: FluentLocalization):
    keyboard = [
        [InlineKeyboardButton(text=l10n.format_value('back-to-start'), callback_data='back_to_start')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)