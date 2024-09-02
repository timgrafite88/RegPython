import csv
import re
from pprint import pprint

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

def format_fio(contact):
    fio_parts = contact[:3]  # берем первые три элемента
    full_fio = " ".join(fio_parts).split()  # объединяем и разбиваем
    if len(full_fio) == 2:  # если только фамилия и имя
        return full_fio[0], full_fio[1], ''
    elif len(full_fio) == 3:  # если фамилия, имя и отчество
        return full_fio[0], full_fio[1], full_fio[2]
    return contact[:3]  # если что-то пошло не так, возвращаем как есть

# Форматирование телефонов
def format_phone(phone):
    phone_pattern = re.compile(
        r'(\+7|8)?\s*\(?(\d{3})\)?\s*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})\s*(?:доб\.?\s*(\d+)|\(?доб\.?\s*(\d+)\)?)?'
    )
    match = phone_pattern.match(phone)
    if match:
        formatted_phone = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
        # Проверяем, есть ли добавочный номер
        if match.group(6):  # если добавочный номер без скобок
            formatted_phone += f" доб.{match.group(6)}"
        elif match.group(7):  # если добавочный номер в скобках
            formatted_phone += f" доб.{match.group(7)}"
        return formatted_phone
    return phone  # если не совпадает, возвращаем как есть


contacts_dict = {}
for contact in contacts_list:
    lastname, firstname, surname = format_fio(contact)
    phone = format_phone(contact[5])

    key = (lastname, firstname)
    if key not in contacts_dict:
        contacts_dict[key] = [lastname, firstname, surname, contact[3], contact[4], phone, contact[6]]
    else:
        # Объединяем информацию (если она отличается)
        existing_contact = contacts_dict[key]
        existing_contact[3] = existing_contact[3] or contact[3]  # organization
        existing_contact[4] = existing_contact[4] or contact[4]  # position
        existing_contact[5] = existing_contact[5] or phone  # phone (если не было)
        existing_contact[6] = existing_contact[6] or contact[6]  # email

# Преобразуем словарь обратно в список
contacts_list = list(contacts_dict.values())

#код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(contacts_list)