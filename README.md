ИНФО
---------
CelebritiesFinder - сервис который позволяет посмотреть на какую знаминитость ты больше всего похож.
--------

Для запуска предварительно необходимо скачать:
  1. Датасет https://drive.google.com/file/d/12bvipsZ4DJtXtxGOurBiFELifogsc7Se/view?usp=sharing

Скачанные папку data необходимо поместить в корень проекта с ботом (TelegramBot)

Все необходимые requirements.txt находятся в папках проекта

Структура
--------
В папке ML находятся скрипты для обработки датасета и получения векторного представления фото

В папке TelegramBot находится реализация бота для телеграмм 

В папке Web находится реализация веб-серверного приложения (Front и Back)

РАБОТА
--------

Для работы Вам понадобиться Python версии 3.11 и выше, 
а также ASP.NET Core Runtime 8.0

--------


ЗАПУСК
--------------

Для того что-бы запустить WebServer на ASP.NET Core Runtime 8.0 и SDK 8.0.203 необходимо
  1) В папке ./Web/Backend/ запустить командную строку.
  2) Ввести команду dotnet build
  3) Ввести команду dotnet run

Для запуска телеграм бота необходимо запустить скрипт TelegramBot/main.py

Для запуска сервера необходимо зайти в папку Web/Front/hackaton/ и ввести команду python manage.py runserver

--------------


ДЕМО
--------------
Видео на демонстрацию работы:
  1. Запись видео в телеграмм боте https://drive.google.com/file/d/1eiBByD-yI_b93ReqyyjB0roNL7SAKLpf/view?usp=sharing
  2. Фотографии в телеграмм боте https://drive.google.com/file/d/118KPW3SUjXTBxfOEZZCIT85mSlyjO2LY/view?usp=sharing
  3. Работа сайта https://drive.google.com/file/d/19BuvJboqB5ypjPeSClZJS8qwOqdEhLKQ/view?usp=sharing
--------------


ПОМОЩЬ
------------
За помощью по установке и использованию проекта можно обратиться в телеграмме:
1) Галицков Богдан @boginc
2) Максимов Максим @maks_maks1
3) Ахунов Олег @olicrab
4) Хазиев Равиль @HAHRAH
5) Нугаев Владислав @sebek008
--------------
