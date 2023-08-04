from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True)
kb_menu.add(KeyboardButton("Поиск собеседника🔎"))
kb_menu.add(KeyboardButton("Сменить пол✏️"))

kb_choise_sex = InlineKeyboardMarkup(row_width=2)
kb_choise_sex.add(InlineKeyboardButton("👨", callback_data='choise_sex_m'), InlineKeyboardButton("👩", callback_data='choise_sex_g'))

kb_choise_edit_sex = InlineKeyboardMarkup(row_width=2)
kb_choise_edit_sex.add(InlineKeyboardButton("👨", callback_data='choise_edit_sex_m'), InlineKeyboardButton("👩", callback_data='choise_edit_sex_g'))

kb_find = ReplyKeyboardMarkup(resize_keyboard=True)
kb_find.add(KeyboardButton("Стоп❌"))

kb_dialog = ReplyKeyboardMarkup(resize_keyboard=True)
kb_dialog.add(KeyboardButton("Закончить диалог❌"))
kb_dialog.add(KeyboardButton("Новый собеседник♻️"))
