from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Загрузить аудиозапись")],
            [KeyboardButton(text="Получить транскрипцию")],
            [KeyboardButton(text="Просмотреть мои записи")]
        ],
        resize_keyboard=True
    )

def generate_audio_keyboard(audio_files):

    cleaned_audio_files = [audio.replace('uploads\\', '') for audio in audio_files]
    buttons = [[KeyboardButton(text=audio)] for audio in cleaned_audio_files]
    buttons.append([KeyboardButton(text='Вернуться')])
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    return keyboard
