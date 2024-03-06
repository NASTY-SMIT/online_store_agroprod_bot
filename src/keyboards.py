from telebot import types

import buttons

back_keyboard = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(buttons.back_btn, callback_data="back")
)

confirm_order_keyboard = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(buttons.yes_btn, callback_data="confirm_order"),
    types.InlineKeyboardButton(buttons.no_btn, callback_data="restart_order")
)

order_types__keyboard = types.InlineKeyboardMarkup(row_width=1).add(
    types.InlineKeyboardButton(
        buttons.boneless_beef_btn, callback_data="order_1"),
    types.InlineKeyboardButton(buttons.beef_meat_btn, callback_data="order_2"),
    types.InlineKeyboardButton(buttons.beef_cut_btn, callback_data="order_3"),
    types.InlineKeyboardButton(buttons.beef_sp_btn, callback_data="order_4")
)

start_keyboard = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton(
        buttons.btn_store_btn, callback_data="assortment"),
    types.InlineKeyboardButton(
        buttons.btn_question_btn, callback_data="question"),
    types.InlineKeyboardButton(
        buttons.placing_order_btn, callback_data="order")
)

assortment_end_keyboard = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton(
        buttons.btn_store_btn, callback_data="assortment"),
    types.InlineKeyboardButton(buttons.back_btn, callback_data="back")
)

assortment_type_beef_keyboard = types.InlineKeyboardMarkup(row_width=1).add(
    types.InlineKeyboardButton(
        buttons.boneless_beef_btn, callback_data="boneless_beef"),
    types.InlineKeyboardButton(
        buttons.beef_meat_btn, callback_data="beef_meat"),
    types.InlineKeyboardButton(
        buttons.beef_cut_btn, callback_data="beef_cut"),
    types.InlineKeyboardButton(
        buttons.beef_sp_btn, callback_data="beef_sp"),
    types.InlineKeyboardButton(
        buttons.back_btn, callback_data="back")
)


def generate_order_types_name_keyboard(order_type, order_data, con):
    """
    Функция для генерации клавиатуры с товарами определенной категории мяса.
    Для заказа.
    """
    order_info = order_data.get(order_type)
    if order_info:
        table_name = order_info["type"]
        btn_text = order_info["button_text"]
        with con:
            data = con.execute(f"SELECT name FROM {table_name}").fetchall()
        markup = types.InlineKeyboardMarkup(row_width=1)
        for index, row in enumerate(data):
            name = row[0]
            callback_data = f"{order_type}_{index}"
            button = types.InlineKeyboardButton(
                name, callback_data=callback_data)
            markup.add(button)

        return markup, btn_text
    return None, None


def generate_keyboard_for_assortment(call_data, con):
    """
    Функция для генерации клавиатуры с товарами определенной категории мяса.
    Для просмотра ассортимента.
    """
    with con:
        data = con.execute(f"SELECT name FROM {call_data}").fetchall()
    markup = types.InlineKeyboardMarkup(row_width=1)
    for index, row in enumerate(data):
        name = row[0]
        callback_data = f"{call_data}_{index}"
        button = types.InlineKeyboardButton(name, callback_data=callback_data)
        markup.add(button)

    return markup
