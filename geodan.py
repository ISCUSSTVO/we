import asyncio
from aiogram import F, Bot, Dispatcher, types
from aiogram.filters import Command
from kivy.app import App
from plyer import gps
from kbds import get_callback_btns
import os
from dotenv import find_dotenv, load_dotenv
from kivy.support import install_twisted_reactor



load_dotenv(find_dotenv())
token = os.getenv("TOKEN")

# Инициализация бота
bot = Bot(token=token)
dp = Dispatcher()

class GeoApp(App):
    def build(self):
        # Конфигурация GPS
        try:
            gps.configure(on_location=self.on_location)
            gps.start()
        except NotImplementedError:
            print("GPS не поддерживается на этом устройстве")
        return  # Пустой интерфейс

    def on_location(self, **kwargs):
        # Сохраняем последние координаты
        self.last_location = (kwargs['lat'], kwargs['lon'])

    async def send_location(self, chat_id):
        if hasattr(self, 'last_location'):
            lat, lon = self.last_location
            await bot.send_location(chat_id=chat_id, latitude=lat, longitude=lon)
        else:
            await bot.send_message(chat_id, "Геоданные недоступны")

# Обработчики для бота
@dp.message(F.text == 'start')
async def start_handler(message: types.Message):
    await message.answer("Нажмите кнопку для получения геоданных:", 
                        reply_markup=get_callback_btns(btns={"📍 Получить геоданные": "get_geodata"}))

@dp.callback_query(F.data == 'get_geodata')
async def get_geodata_handler(callback: types.CallbackQuery):
    geo_app = GeoApp.get_running_app()
    await geo_app.send_location(callback.from_user.id)
    await callback.answer()

@dp.message(Command("stop"))
async def stop_app(message: types.Message):
    await message.answer("Приложение закрывается...")
    os._exit(0) 

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    # Запуск Kivy и бота в разных потоках
    from threading import Thread

    geo_app = GeoApp()
    Thread(target=geo_app.run).start()
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    install_twisted_reactor()