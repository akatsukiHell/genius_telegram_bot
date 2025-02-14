import aiogram
from contextlib import suppress


from aiogram import Bot, Router, F
import aiogram.exceptions
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage

from fluent.runtime import FluentLocalization
from keyboards.inline_keyboard import back_button, menu_buttons

from middlewares.throttling import ThrottlingMiddleware

router = Router()

@router.callback_query(F.data == "back_to_start")
async def back_to_menu(callback: CallbackQuery ,l10n: FluentLocalization, state: FSMContext):
   await callback.message.edit_text(l10n.format_value("start-text"), reply_markup=menu_buttons(l10n))
   await state.clear()
   await callback.answer()

@router.callback_query(F.data == "change_to_eng")
async def change_to_english(callback: CallbackQuery, l10n: FluentLocalization):
   await callback.message.edit_text("Функция в разработке!", reply_markup=back_button(l10n))
   await callback.answer()



storage = RedisStorage.from_url('redis://localhost:6379/0')

class getAlbumLink(StatesGroup):
   album_link = State()


class chatInfo(StatesGroup):
   chat_id = State()
   message_id = State()


@router.callback_query(F.data == "tracklist_markup")
async def album_link(callback: CallbackQuery, l10n: FluentLocalization, state: FSMContext):

   await state.update_data(
      chat_id = callback.message.chat.id, message_id = callback.message.message_id
   )

   await state.set_state(getAlbumLink.album_link)
   await callback.message.edit_text(l10n.format_value("track-list-info"), reply_markup=back_button(l10n))
   await callback.answer()

@router.message(getAlbumLink.album_link)
async def return_parsing_album(message: Message, l10n: FluentLocalization, state: FSMContext, bot: Bot):

   await state.update_data(album_link = message.text)

   data = await state.get_data()
   with suppress(aiogram.exceptions.TelegramBadRequest):
      await bot.delete_message(data.get('chat_id'), data.get('message_id'))

      router.message.middleware(ThrottlingMiddleware(storage=storage))

   if "genius.com/albums" not in message.text:
      msg = await message.answer(
         '<b>Некорректная ссылка!</b>\n\nОтправь новую ссылку, или вернись в главное меню 👇🏻', reply_markup=back_button(l10n)
      )
      await state.update_data(message_id = msg.message_id)
   else:
      await message.answer("Ссылка корректна! Ожидайте результат", reply_markup=back_button(l10n))
      await state.clear()

        




