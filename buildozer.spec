[app]
title = GeoBot
package.name = geobot
package.domain = org.example
version = 1.0
source.dir = .
source.include_exts = py, env
requirements = 
    python3,
    kivy,
    plyer,
    requests,
    aiogram,
    aiohttp,
    python-dotenv,
    openssl,
    certifi

android.permissions = INTERNET, ACCESS_COARSE_LOCATION, ACCESS_FINE_LOCATION
android.api = 34
android.ndk = 25b
orientation = portrait

# Добавьте эти секции
[buildozer]
log_level = 2

# Для работы с env файлом
source.include_patterns = *.env

# Для асинхронных библиотек
p4a.branch = develop
android.arch = armeabi-v7a