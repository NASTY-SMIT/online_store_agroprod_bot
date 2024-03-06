import buttons

user_states = {}

last_messages = {}

user_data = {}

order_data = {
    "order_1": {
        "type": "boneless_beef", "button_text": buttons.boneless_beef_btn
        },
    "order_2": {
        "type": "beef_meat", "button_text": buttons.beef_meat_btn
        },
    "order_3": {
        "type": "beef_cut", "button_text": buttons.beef_cut_btn
        },
    "order_4": {
        "type": "beef_sp", "button_text": buttons.beef_sp_btn
        }
}

beef_type_data = {
    "boneless_beef": buttons.boneless_beef_btn,
    "beef_meat": buttons.beef_meat_btn,
    "beef_cut": buttons.beef_cut_btn,
    "beef_sp": buttons.beef_sp_btn
}

table_file_mapping = {
    "boneless_beef": "data_boneless_beef.txt",
    "beef_meat": "data_beef_meat.txt",
    "beef_cut": "data_beef_cut.txt",
    "beef_sp": "data_beef_sp.txt",
}
