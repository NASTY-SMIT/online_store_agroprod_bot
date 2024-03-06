# Telegram-Бот Торгового дома "Агропрод"

# Функционал проекта
#### Заполнение базы данных из заранее подготовленных файлов
> В папке src/data подготовлены .txt файлы, в которых хранится весь ассортимент товаров "Агропрод". При запуске sql.py все файлы читаются и данные записываются в соответсвующие по названиям таблицы.

#### Просмотр ассортимента
> Каждый пользователь может нажать на кнопку "Посмотреть ассортимент", выбрать соответсвующую категорию и нужный товар. После этого ему придет сообщение с подробным описанием интересующего товара.

#### Задать вопрос
> Любой пользователь может через бота задать интересующий вопрос, на который ответит администация "Агропрод".

#### Оформление заказа
> Каждый пользователь может нажать на кнопку "Сделать заказ", после чего ему будет предложено сначала заполнить свой профиль, потом он сможет оформить свой заказ. Личные данные пользователя проходят валидацию перед тем, как попасть в базу данных.

## Используемый стек

- Python
- Telebot
- Docker

## Архитектура проекта

| Директория    | Описание                                                |
|---------------|---------------------------------------------------------|
| `src`         | Код бота                                                |
| `src/data`    | Данные, для выгрузки в базу данных                      |
| `src/images`  | Фотографии ассортимента всех видов мяса                 |

# Подготовка

## Требования

1. **Python 3.10**  

2. **Docker**
[Документация](https://docs.docker.com/)
[Установка docker на Linux](https://docs.docker.com/engine/install/ubuntu/)
[Установка docker на Windows](https://docs.docker.com/desktop/install/windows-install/)
3. **Токен Telegram бота**  
   [Документация](https://core.telegram.org/bots/features#botfather)  
   Перед запуском нужно получить **token** у бота
   [@BotFather](https://t.me/BotFather). После того как бот будет
   зарегестрирован - вам выдадут **token**, его нужно добавить в файл `.env`,
   строку `TOKEN=`. Смотреть пример в документе `env.example`.  
   *Про более подробное создание бота читать в приложенной документации.*

## Стиль кода [black style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)

# Разворачиваем проект в контейнерах
Создаём `.env` файл в корневой директории проекта и заполняем его по
образцу `.env.example`

Переходим в корневую директорию проекта

```shell
cd online_store_agroprod_bot
```

Поднимаем контейнеры
```shell
sudo docker-compose up --build
```

# Разворачиваем проект локально

Переходим в корневую директорию проекта

```shell
cd online_store_agroprod_bot
```
Cоздаем и активируем виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```
Устанавливаем зависимости
```shell
pip install -r requirements.txt
```

Создаём `.env` файл в корневой директории проекта и заполняем его по
образцу `.env.example`

Переходим в директорию `src`

```shell
cd src
```

Создаем и заполняем базу данных

```shell
python sql.py
```

Запускаем бота

Перед выполнением команд откройте новый терминал
(не забываем добавить **token** бота в файл `.env`, строку `TOKEN=`)

```shell
python bot.py
```

❤️Автор [Nasty Shmidt](https://github.com/NASTY-SMIT)❤️
[Обратная связь](https://t.me/nastyShmidt) - Telegram