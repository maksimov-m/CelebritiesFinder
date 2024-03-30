import asyncio
import os
import pandas as pd
from aiogram import Bot, Dispatcher, types
from photo_detector import photo_detector
from video_detector import video_detect
import cv2
# Создаем экземпляр бота и диспетчера
bot_token = '6467262183:AAHwRJW6hJ8vW86PIGsnFoYMi8zBlsX4OAE'
bot = Bot(token=bot_token)
dp = Dispatcher(bot)
SERVER_URL = "http://26.221.175.97:5116/api/sendPhotoWithURL"
# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Отправь мне фото, видео или голосовое сообщение, а я скажу, на кого ты похож 😉")

# Обработчик медиафайлов (фото и видео)
@dp.message_handler(content_types=['photo','video','video_note'])
async def media_handler(message: types.Message):
    if message.photo:
        file_id=message.photo[-1].file_id
    elif message.video:
        file_id = message.video.file_id
    elif message.video_note:
        file_id = message.video_note.file_id
    else:
        await message.reply("Мне нужно фото или видео, а не что-то другое.")
        return

    # Путь для сохранения медиафайла
    file_path=os.path.join('media',f"{file_id}.jpg" if message.photo else f"{file_id}.mp4")
    if(message.photo):
        await save_media(message.photo[-1],file_path)
        flag=False
    elif (message.video):
        await save_media(message.video, file_path)
        flag = True
    else:
        await save_media(message.video_note,file_path)
        flag = True
    # Сохраняем медиафайл в папку
    await message.reply("Спасибо! Мы получили ваш медиафайл и начали его обработку.")
    await send_media_and_info_to_chat(message,file_path, flag)
#отправляем фото/видео и всю информацию в телеграмбота
async def send_media_and_info_to_chat(message: types.Message,file_path, flag):
    #два варианта работы алгоритма для фото и для видео
    if not flag:
        result = photo_detector(file_path)
        if result is None:
            await message.answer("Лиц не найдено")
            return
        for (x, y, w, h), d_res in result:
            print(d_res)
            cv2.imwrite("./media/tmp.jpg", cv2.imread(file_path)[y:y + h, x:x + w])

            with open("./media/tmp.jpg", 'rb') as photo:
                await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo
                )

            persons = d_res['class']
            probs = d_res['prob']
            await message.answer("Вот на кого ты больше всего похож по нашему мнению😉")

            df = pd.read_csv("ussr_russia.csv", sep=";")

            with open("ussr_russia.csv", "r", encoding="utf-8") as file:

                for pers, prob in zip(persons, probs):

                    tmp = df[df['id'] == int(pers)]

                    # Получаем информацию о личности
                    name = tmp["name"].values
                    link = tmp["link"].values
                    specialization = tmp["specialization"].values
                    films_years = tmp["films_years"].values
                    description = tmp["description"].values

                    # Определяем путь к фотографии
                    photo_path = os.path.join(f"data/{pers}", '1.jpg')
                    if not os.path.exists(photo_path):
                        continue

                    # Открываем фотографию
                    with open(photo_path, 'rb') as photo_file:
                        # Отправляем фото и информацию о личности в чат
                        await bot.send_photo(
                            chat_id=message.chat.id,
                            photo=photo_file,
                            caption=f"Процент похожести: {prob}%\nИмя: {name[0]}\nСсылка: {link[0]}\nСпециализация: {specialization[0]}\nГоды съемок: {films_years[0]}\nОписание: {description[0]}"
                        )

    else:
        d_res = video_detect(file_path)
        persons = d_res['class']
        probs = d_res['prob']
        await message.answer("Вот на кого ты больше всего похож по нашему мнению😉")

        df = pd.read_csv("ussr_russia.csv", sep=";")

        with open("ussr_russia.csv", "r", encoding="utf-8") as file:

            for pers, prob in zip(persons, probs):

                tmp = df[df['id'] == int(pers)]

                # Получаем информацию о личности
                name = tmp["name"].values
                link = tmp["link"].values
                specialization = tmp["specialization"].values
                films_years = tmp["films_years"].values
                description = tmp["description"].values

                # Определяем путь к фотографии
                photo_path = os.path.join(f"data/{pers}", '1.jpg')
                if not os.path.exists(photo_path):
                    continue

                # Открываем фотографию
                with open(photo_path, 'rb') as photo_file:

                    # Отправляем фото и информацию о личности в чат
                    await bot.send_photo(
                        chat_id=message.chat.id,
                        photo=photo_file,
                        caption=f"Процент похожести: {prob}%\nИмя: {name[0]}\nСсылка: {link[0]}\nСпециализация: {specialization[0]}\nГоды съемок: {films_years[0]}\nОписание: {description[0]}"
                    )


# Функция для сохранения фотографии в папку
async def save_media(media,file_path):
    with open(file_path, 'wb') as file:
        await media.download(file)
async def main():
    await dp.start_polling()
    await asyncio.sleep(3600)
    await dp.stop_polling()

if __name__ == '__main__':
    asyncio.run(main())
