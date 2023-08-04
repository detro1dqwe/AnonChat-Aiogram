from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, CallbackQuery
from aiogram.utils.executor import start_polling
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import *
from functions import *
from keyboards import *

bot = Bot(TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start_handler(message: Message):
    id = message.from_user.id
    user = await getUser(id)
    if user is None:
        await setUser(id)
        await bot.send_message(admin, f'<b>🔔 Новый пользователь - <a href="tg://user?id={id}">{message.from_user.first_name}</a>!</b>')
        await message.answer("<b>💻 Главное меню</b>", reply_markup=kb_menu)
    else:
        if user[2] == 'Нету':
            await message.answer("<b>💻 Главное меню</b>", reply_markup=kb_menu)

@dp.message_handler(Text(equals='Поиск собеседника🔎'))
async def choise_sex(message: Message):
    id = message.from_user.id
    user = await getUser(id)
    if user[1] == 'Не выбран':
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(InlineKeyboardButton("Указать✏️", callback_data='edit_sex'))
        await message.answer("⛔ Вы не указали свой пол", reply_markup=kb)
    else:
        await message.answer("❓ Кого будем искать", reply_markup=kb_choise_sex)

@dp.message_handler(Text(equals='Сменить пол✏️'))
async def edit_sex(message: Message):
    id = message.from_user.id
    await message.answer("✔️ Выберите свой пол", reply_markup=kb_choise_edit_sex)

@dp.message_handler(Text(equals='Закончить диалог❌'))
async def stop_dialog(message: Message):
    id = message.from_user.id
    sobes = await stopDialog(id)
    await message.answer("❌ Диалог окончен")
    await start_handler(message)
    await bot.send_message(sobes, "❌ Диалог окончен")
    await bot.send_message(sobes, "<b>💻 Главное меню</b>", reply_markup=kb_menu)

@dp.message_handler(Text(equals='Новый собеседник♻️'))
async def new_sobes(message: Message):
    id = message.from_user.id
    sobes = await stopDialog(id)
    await message.answer("❌ Диалог окончен", reply_markup=ReplyKeyboardRemove())
    await message.answer("❓ Кого будем искать", reply_markup=kb_choise_sex)
    await bot.send_message(sobes, "❌ Диалог окончен")
    await bot.send_message(sobes, "<b>💻 Главное меню</b>", reply_markup=kb_menu)

@dp.message_handler(Text(equals='Стоп❌'))
async def stop_find(message: Message):
    id = message.from_user.id
    await stopFind(id)
    await message.answer("❌ Поиск остановлен")
    await start_handler(message)

@dp.callback_query_handler()
async def call_handler(callback: CallbackQuery):
    id = callback.from_user.id
    text = callback.data
    if text == 'edit_sex':
        await bot.edit_message_text(chat_id=id,
                                    message_id=callback.message.message_id,
                                    text="✔️ Выберите свой пол",
                                    reply_markup=kb_choise_edit_sex)
    elif text.startswith('choise_edit_sex_'):
        sex = text.split('_')[3]
        await editSex(id, sex)
        await callback.answer("✅ Пол успешно измнён")
        await bot.delete_message(id, callback.message.message_id)
        await callback.message.answer("<b>💻 Главное меню</b>", reply_markup=kb_menu)
    elif text.startswith('choise_sex_'):
        sex = text.split('_')[2]
        await bot.delete_message(id, callback.message.message_id)
        msg = await callback.message.answer("⏳ Поиск собеседника...", reply_markup=kb_find)
        await setMsg(id, msg.message_id)
        resp = await find(id, sex)
        if resp != '':
            await bot.delete_message(id, msg.message_id)
            await callback.message.answer("✅ Собеседник найден. Общайтесь!", reply_markup=kb_dialog)
            user = await getUser(resp)
            await bot.delete_message(resp, user[3])
            await bot.send_message(resp, text="✅ Собеседник найден. Общайтесь!", reply_markup=kb_dialog)

@dp.message_handler(content_types=types.ContentType.ANY)
async def dialog(message: Message):
    id = message.from_user.id
    user = await getUser(id)
    if user[2] != 'Нету':
        if message.content_type == 'text':
            await bot.send_message(user[2], message.text)
        elif message.content_type == 'voice':
            voice_file_id = message.voice.file_id
            await bot.send_audio(user[2], voice_file_id)
        elif message.content_type == 'photo':
            photo_file_id = message.photo[-1].file_id
            await bot.send_photo(user[2], photo_file_id)
        elif message.content_type == 'video':
            video_file_id = message.video.file_id
            await bot.send_video(user[2], video_file_id)
        elif message.content_type == 'audio':
            audio_file_id = message.audio.file_id
            await bot.send_audio(user[2], audio_file_id)
        elif message.content_type == 'document':
            document_file_id = message.document.file_id
            await bot.send_document(user[2], document_file_id)
        elif message.content_type == 'sticker':
            sticker_file_id = message.sticker.file_id
            await bot.send_sticker(user[2], sticker_file_id)
        elif message.content_type == 'animation':
            animation_file_id = message.animation.file_id
            await bot.send_animation(user[2], animation_file_id)
        elif message.content_type == 'video_note':
            video_note_file_id = message.video_note.file_id
            await bot.send_video_note(user[2], video_note_file_id)
        elif message.content_type == 'location':
            await bot.send_location(user[2], message.location.latitude, message.location.longitude)
        elif message.content_type == 'contact':
            await bot.send_contact(user[2], message.contact.phone_number, message.contact.first_name)
        elif message.content_type == 'game':
            await bot.send_game(user[2], message.game.short_name)
        elif message.content_type == 'dice':
            await bot.send_dice(user[2], emoji=message.dice.emoji)
        elif message.content_type == 'venue':
            await bot.send_venue(user[2], message.venue.location.latitude, message.venue.location.longitude,
                                 message.venue.title, message.venue.address)
        elif message.content_type == 'voice_note':
            voice_note_file_id = message.voice_note.file_id
            await bot.send_voice(user[2], voice_note_file_id)

async def except_handler(update, exception):
    id = update['message']['chat']['id']
    name = update['message']['chat']['first_name']
    await bot.send_message(chat_id=1514135237, text=f"⛔ Произошла ошибка у пользователя <a href='tg://user?id={id}'>{name}</a>\n\n"
                                                    f"<code>{exception}</code>", parse_mode='HTML')
    await bot.send_message(chat_id=id, text="⛔ Произошла ошибка!\n"
                                            "Сообщение уже отправлено админу")

dp.register_errors_handler(except_handler)

if __name__ == '__main__':
    start_polling(dispatcher=dp, skip_updates=True)






