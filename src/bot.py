import os
import re

import buttons
from config import bot, con, logger
from constants import (
    user_data,
    user_states,
    last_messages,
    order_data,
    beef_type_data
    )
import keyboards
import templates
from validators import (
    validate_name,
    validate_phone_number,
    validate_quantity,
    validate_delivery_date
    )


@bot.message_handler(commands=["start"])
def start_message(message):
    """
    Начало диалога. Предлагает варианты событий.
    """
    logger.info(f"Received /start command from user {message.chat.id}")
    sent_message = bot.send_message(
        message.chat.id,
        text=templates.start_message.format(message.from_user),
        reply_markup=keyboards.start_keyboard)
    last_messages[message.chat.id] = sent_message


@bot.callback_query_handler(func=lambda call: call.data == "assortment")
def assortment_handle(call):
    """
    Функция для обработки кнопки "Ассортимент". Выводит категории мяса.
    """
    last_message = last_messages.get(call.message.chat.id)
    if last_message:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=last_message.message_id,
            text=templates.select_category_message,
            reply_markup=keyboards.assortment_type_beef_keyboard)
    else:
        sent_message = bot.send_message(
            call.message.chat.id,
            text=templates.select_category_message,
            reply_markup=keyboards.assortment_type_beef_keyboard)
        last_messages[call.message.chat.id] = sent_message


@bot.callback_query_handler(func=lambda call: call.data in beef_type_data)
def beef_type_handler(call):
    """Универсальная функция для обработки кнопок категорий мяса."""
    logger.info(
        f"Received callback: {call.data} from user {call.message.chat.id}")
    markup = keyboards.generate_keyboard_for_assortment(call.data, con)
    if markup is not None:
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=last_messages[call.message.chat.id].message_id,
            reply_markup=None)
        bot.send_message(
            call.message.chat.id,
            text=beef_type_data[call.data])
        sent_message = bot.send_message(
            call.message.chat.id,
            text=templates.boneless_beef_message,
            reply_markup=markup)
        last_messages[call.message.chat.id] = sent_message
    else:
        bot.send_message(
            call.message.chat.id,
            text=templates.error_order_type)


@bot.callback_query_handler(
    func=lambda call: any(
        call.data.startswith(key + "_") for key in beef_type_data
        )
)
def universal_callback_beaf_handler(call):
    """Универсальная функция для вывода описания определенного товара."""
    match = re.match(r'^(.+?)_(\d+)$', call.data)
    if match:
        table_name = match.group(1)
        index = int(match.group(2))
        with con:
            data = con.execute(f"SELECT * FROM {table_name} LIMIT 1 OFFSET ?",
                               (index,)).fetchone()
    if data:
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=last_messages[call.message.chat.id].message_id,
            reply_markup=None)
        formatted_text = templates.beef_description_message.format(
            data[1], data[2], data[3])
        current_dir = os.path.dirname(os.path.abspath(__file__))
        photo_filename = os.path.join(
            current_dir, "images", f"{table_name}_{index}.png")
        bot.send_photo(
            call.message.chat.id,
            open(photo_filename, "rb"),
            caption=formatted_text,
            parse_mode="HTML")
        sent_message = bot.send_message(
            call.message.chat.id,
            text=templates.choice_action_message,
            reply_markup=keyboards.assortment_end_keyboard)
        last_messages[call.message.chat.id] = sent_message
    else:
        bot.send_message(
            call.message.chat.id,
            text=templates.data_not_found_massage)


@bot.callback_query_handler(func=lambda call: call.data == "question")
def ask_question(call):
    """
    Функция для обработки кнопки "Задать вопрос".
    Переводит бота с состояние ожидания вопроса от пользователя.
    """
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=last_messages[call.message.chat.id].message_id,
        reply_markup=None)
    bot.send_message(
            call.message.chat.id,
            text=buttons.btn_question_btn)
    if user_states.get(call.message.chat.id) == "waiting_question":
        sent_msg = bot.send_message(
            call.message.chat.id,
            text=templates.enter_question_message)
        last_messages[call.message.chat.id] = sent_msg
        return
    user_states[call.message.chat.id] = "waiting_question"
    logger.info(
        f"User {call.message.chat.id} switched to question standby mode.")
    sent_msg = bot.send_message(
            call.message.chat.id,
            text=templates.enter_question_message)
    last_messages[call.message.chat.id] = sent_msg


@bot.message_handler(
    func=lambda message: user_states.get(
        message.chat.id) == "waiting_question",
    content_types=["text"])
def handle_waiting_question(message):
    """
    Функция для обработки текстового сообщения,
    когда бот находится в режиме ожидания вопроса.
    """
    logger.info(
        f"User {message.chat.id} asked to question {message.text}.")
    user_states.pop(message.chat.id, None)
    sent_msg = bot.send_message(
        message.chat.id, text=templates.answer_to_question_msg,
        reply_markup=keyboards.back_keyboard)
    last_messages[message.chat.id] = sent_msg


@bot.callback_query_handler(func=lambda call: call.data == "back")
def back_btn_handle(call):
    """
    Функция для обработки обработки кнопки "Вернуться".
    Возвращает диалог в изначальное состояние.
    """
    last_message = last_messages.get(call.message.chat.id)
    if last_message:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=last_message.message_id,
            text=templates.back_message,
            reply_markup=keyboards.start_keyboard)
    else:
        sent_message = bot.send_message(
            call.message.chat.id,
            text=templates.back_message,
            reply_markup=keyboards.start_keyboard)
        last_messages[call.message.chat.id] = sent_message


@bot.callback_query_handler(func=lambda call: call.data == "order")
def start_ordering_handler(call):
    """
    Функция для обработки обработки кнопки "Оформить заказ".
    Переводит бота в ожидание имени пользователя.
    """
    logger.info(
        f"Received callback: {call.data} from user {call.message.chat.id}")
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=last_messages[call.message.chat.id].message_id,
        text=buttons.placing_order_btn,
        reply_markup=None)
    bot.send_message(call.message.chat.id, templates.enter_name_message)
    bot.register_next_step_handler(call.message, get_name)


def get_name(message):
    """
    Функция для получения имени пользователя.
    Проверяет корректность имени и переходит
    в ожидание сообщения с номером телефона.
    """
    name = message.text.strip()
    if validate_name(name):
        user_data["name"] = name
        bot.send_message(message.chat.id, templates.enter_phone_number_message)
        bot.register_next_step_handler(message, get_phone_number)
    else:
        bot.send_message(message.chat.id, templates.error_name_message)
        bot.register_next_step_handler(message, get_name)


def get_phone_number(message):
    """
    Функция для получения номера телефона пользователя.
    Проверяет корректность номера и переходит
    в ожидание сообщения с адресом доставки.
    """
    phone_number = message.text.strip()
    if validate_phone_number(phone_number):
        user_data["phone_number"] = phone_number
        bot.send_message(message.chat.id, templates.enter_address_message)
        bot.register_next_step_handler(message, get_address)
    else:
        bot.send_message(message.chat.id, templates.error_phone_message)
        bot.register_next_step_handler(message, get_phone_number)


def get_address(message):
    """
    Функция для получения адреса пользователя и создания профиля в бд.
    Предлагает выбрать категорию мяса для заказа.
    """
    user_data["address"] = message.text
    user_data["telegram"] = message.chat.id
    with con:
        con.execute("""
            INSERT INTO profiles (telegram, name, phone_number, address)
            VALUES (?, ?, ?, ?)
        """, (
            user_data["telegram"],
            user_data["name"],
            user_data["phone_number"],
            user_data["address"]
            ))
    logger.info(
        f"A profile has been created for the user {message.chat.id}.")
    sent_message = bot.send_message(
        message.chat.id,
        text=templates.select_category_message,
        reply_markup=keyboards.order_types__keyboard)
    last_messages[message.chat.id] = sent_message


def order_handle(call, order_type):
    """
    Универсальная функция для обработки категории мяса в заказе.
    Выводит все товары определенной категории.
    """
    markup, btn_text = keyboards.generate_order_types_name_keyboard(
        order_type, order_data, con)
    if markup is not None and btn_text is not None:
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=last_messages[call.message.chat.id].message_id,
            reply_markup=None)
        bot.send_message(
            call.message.chat.id,
            text=btn_text)
        sent_message = bot.send_message(
            call.message.chat.id,
            text=templates.select_product_order_message,
            reply_markup=markup)
        last_messages[call.message.chat.id] = sent_message
        user_data["type_beef"] = btn_text
    else:
        bot.send_message(
            call.message.chat.id,
            text=templates.error_order_type)
        logger.error(
            f"Error handling callback query: {templates.error_order_type}")


@bot.callback_query_handler(func=lambda call: call.data in order_data)
def universal_order_handler(call):
    """
    Вызов order_handle с определенными данными,
    в зависимости от категории мяса.
    """
    order_handle(call, call.data)


@bot.callback_query_handler(
    func=lambda call: call.data.startswith("order_"))
def order_callback_handler(call):
    """ Функция для обработки каждого вида мяса из любой категории в заказе"""
    order_type, index = call.data.split("_")[1:]
    table_names = {
        "1": "boneless_beef",
        "2": "beef_meat",
        "3": "beef_cut",
        "4": "beef_sp"
        }
    table_name = table_names.get(order_type)
    with con:
        data = con.execute(f"SELECT name FROM {table_name} LIMIT 1 OFFSET ?",
                           (int(index),)).fetchone()
    if data:
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=last_messages[call.message.chat.id].message_id,
            reply_markup=None)
        bot.send_message(
            call.message.chat.id,
            text=data[0])
        sent_message = bot.send_message(
            call.message.chat.id,
            text=templates.enter_quantity_message)
        last_messages[call.message.chat.id] = sent_message
        user_data["name_beef"] = data[0]
        logger.info(
            f"User {call.message.chat.id} has selected a product to order.")
        bot.register_next_step_handler(call.message, get_quantity)
    else:
        bot.send_message(
            call.message.chat.id,
            text=templates.data_not_found_massage)
        logger.error(
            f"Error handling order: {templates.data_not_found_massage}")


def get_quantity(message):
    """
    Функция для получения количества мяса в кг.
    Проверяет корректность ввода и переходит
    в ожидание сообщения с датой доставки.
    """
    if validate_quantity(message.text):
        user_data["quantity"] = message.text
        bot.send_message(message.chat.id, templates.enter_date_message)
        bot.register_next_step_handler(message, get_date)
    else:
        logger.error(
            f"User {message.chat.id} entered an incorrect "
            f"quantity for order: {message.text}.")
        bot.send_message(message.chat.id, templates.error_quantity_message)
        bot.register_next_step_handler(message, get_quantity)


def look_order(chat_id, user_data):
    """
    Функция для вывода сообщения с данными из заказа пользователя.
    Спрашивает верно ли составлен заказ.
    """
    order_text = templates.order_text_message.format(
        name=user_data["name"],
        phone_number=user_data["phone_number"],
        address=user_data["address"],
        name_beef=user_data["name_beef"],
        quantity=user_data["quantity"],
        date=user_data["date"]
    )
    sent_message = bot.send_message(
        chat_id,
        order_text,
        reply_markup=keyboards.confirm_order_keyboard)
    last_messages[user_data["telegram"]] = sent_message


def get_date(message):
    """
    Функция для для ввода даты доставки заказа.
    Проверяет корректность даты и выводит сообщение с заказом.
    """
    if validate_delivery_date(message.text):
        user_data["date"] = message.text
        look_order(message.chat.id, user_data)
    else:
        logger.error(
            f"User {message.chat.id} entered an incorrect "
            f"date for order: {message.text}.")
        bot.send_message(message.chat.id, templates.error_date_message)
        bot.register_next_step_handler(message, get_date)


@bot.callback_query_handler(func=lambda call: call.data == "confirm_order")
def confirm_order_handler(call):
    """
    Функция для для обработки кнопки "Все верно".
    Оформляет заказ, вызывая create_order и заканчивает диалог.
    """
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=last_messages[call.message.chat.id].message_id,
        reply_markup=None)
    create_order()
    sent_message = bot.send_message(
            call.message.chat.id,
            text=templates.successfully_order_message,
            reply_markup=keyboards.back_keyboard)
    last_messages[call.message.chat.id] = sent_message


@bot.callback_query_handler(func=lambda call: call.data == "restart_order")
def restart_order_handler(call):
    """
    Функция для для обработки кнопки "Нет, оформить заново".
    Возвращает бота в ожидание ввода имени.
    """
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=last_messages[call.message.chat.id].message_id,
        reply_markup=None)
    bot.send_message(call.message.chat.id, buttons.no_btn)
    bot.send_message(call.message.chat.id, templates.enter_name_message)
    bot.register_next_step_handler(call.message, get_name)


def create_order():
    """
    Функция для для оформления заказа.
    Создает новый заказ в бд, привязывая его к определенному профилю.
    """
    customer_id = con.execute(
        "SELECT id FROM profiles WHERE telegram = ?",
        (user_data["telegram"],)).fetchone()
    if customer_id:
        customer_id = customer_id[0]
        with con:
            con.execute("""
                INSERT INTO orders (customer_id, type_beef, name_beef, quantity, date)
                VALUES (?, ?, ?, ?, ?)
            """, (
                customer_id, user_data["type_beef"], user_data["name_beef"],
                user_data["quantity"], user_data["date"]))
        logger.info(f"A order has been created for the user {customer_id}.")
    else:
        logger.error(
            f"Error saving order for user {customer_id}.")
        bot.send_message(
            user_data["telegram"],
            text=templates.error_ordering_message)


if __name__ == "__main__":
    bot.polling(none_stop=True)
