#main.py
from pprint import pprint
import csv
import re

with open('phonebook_raw.csv', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

for row in contacts_list[1:]:
    for index, item in enumerate(row):
        pattern = r'\s'
        result = item.strip()
        row[index] = result
        if 'доб.' in item:
            pattern = r'(\+7|8)\s?(\(?(\d{3})\)?)[^0-9]?(\d{3})[^0-9]?' \
                      r'(\d{2})[^0-9]?(\d+)\s?\(?доб.\s?(\d+)\)?'
            u = r'+7(\3)\4-\5-\6 доб.\7'
            result = re.sub(pattern, u, item)
            row[index] = result
        else:
            pattern = r'(\+7|8)\s?(\(?(\d{3})\)?)[^0-9]?(\d{3})[^0-9]?(\d{2})[^0-9]?(\d+)'
            u = r'+7(\3)\4-\5-\6'
            result = re.sub(pattern, u, item)
            row[index] = result

for row in contacts_list[1:]:
    for index, item in enumerate(row[:3]):
        pattern = r'\s'
        if item == '':
            del row[index]
        elif len(re.findall(pattern, item)) == 1:
            result = item.split(' ')
            row[index] = result[0]
            row[index + 1] = result[1]
            break
        elif len(re.findall(pattern, item)) == 2:
            result = item.split(' ')
            row[index] = result[0]
            row[index + 1] = result[1]
            row[index + 2] = result[2]
            break

repeat_list = []
for row in contacts_list[1:]:
    for row_ in contacts_list[contacts_list.index(row) + 1:]:
        if row[0] == row_[0] and row[1] == row_[1]:
            for index, item in enumerate(row):
                if item == '' and row_[index] != '':
                    row[index] = row_[index]
            repeat_list.append(row_)
for row in contacts_list[1:]:
    if row in repeat_list:
        contacts_list.remove(row)

with open("phonebook.csv", "w", encoding='utf-8', newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)


from pprint import pprint
import re
import csv

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", 'r', newline='', encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
#pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
# ваш код
# создаем паттерны
pattern_full_name = re.compile(r'([А-ЯЁ]\w+)\W+([А-ЯЁ]\w+)\W+([А-ЯЁ]\w+)')
pattern_short_name = re.compile(r'([А-ЯЁ]\w+)\W+([А-ЯЁ]\w+)')
pattern_organization = re.compile(r'([А-ЯЁ]\w+)')
pattern_phone = re.compile(r'(\+7|8)\s?(\([\d]+\))?\s?([\d|\-]+)([\s\(]*)(доб)?[\s.]*([\d]+)?[)]?')
pattern_email = re.compile(r'[^\,\s]+[@]\w+\.\w+')

correct_list = []
contacts_list.pop(0)
item_list = []

# преобразуем вложенные списки в строки путем сшивания
for contact in contacts_list:
    item = ''
    for note in contact:
        item += note + ', '
    item_list.append(item)

# ищем паттерны в строках, заносим найденные значения в словарь
for item in item_list:
    contact_dict = {
        'lastname': '',
        'firstname': '',
        'surname': '',
        'organization': '',
        'position': '',
        'phone': '',
        'email': ''
    }

    if pattern_full_name.search(item):
        contact_dict['lastname'] = pattern_full_name.search(item).group(1)
        contact_dict['firstname'] = pattern_full_name.search(item).group(2)
        contact_dict['surname'] = pattern_full_name.search(item).group(3)
        item = item.replace(pattern_full_name.search(item).group(0), '')
    elif pattern_short_name.search(item):
        contact_dict['lastname'] = pattern_short_name.search(item).group(1)
        contact_dict['firstname'] = pattern_short_name.search(item).group(2)
        contact_dict['surname'] = ''
        item = item.replace(pattern_short_name.search(item).group(0), '')

    if pattern_organization.search(item):
        contact_dict['organization'] = pattern_organization.search(item).group(1)
        item = item.replace(pattern_organization.search(item).group(0), '')

    if pattern_phone.search(item):
        prefix = '+7'
        if pattern_phone.search(item).group(2):
            code = pattern_phone.search(item).group(2)
            dirty_number = pattern_phone.search(item).group(3)
            number = dirty_number.replace('-', '')
            number = number[0:3] + '-' + number[3:5] + '-' + number[5:7]
        else:
            code = '(' + pattern_phone.search(item).group(3)[0:3] + ')'
            dirty_number = pattern_phone.search(item).group(3)[3:]
            number = dirty_number.replace('-', '')
            number = number[0:3] + '-' + number[3:5] + '-' + number[5:7]
        if pattern_phone.search(item).group(6):
            additional = ' доб.' + pattern_phone.search(item).group(6)

        else:
            additional = ''
        phone = prefix + code + number + additional
        contact_dict['phone'] = phone
        item = item.replace(pattern_phone.search(item).group(0), '')

    if pattern_email.search(item):
        contact_dict['email'] = pattern_email.search(item).group(0)
        item = item.replace(pattern_email.search(item).group(0), '')

    item = item.replace(',', '')
    contact_dict['position'] = item.strip()

    correct_list.append(contact_dict)

# объединяем дубликаты контактов
index_of_double = []
for i in range(len(correct_list)):
    for j in range(i+1, len(correct_list)):
        if correct_list[i]['firstname'] == correct_list[j]['firstname'] and \
                correct_list[i]['lastname'] == correct_list[j]['lastname']:
            for key in correct_list[i].keys():
                if correct_list[i][key] == '':
                    correct_list[i][key] = correct_list[j][key]
            index_of_double.append(j)

final_list = [['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']]

# удаляем дубликаты контактов, преобразуем словарь в список в нужной последовательности
for i in range(len(correct_list)):
    if i not in index_of_double:
        person = []
        person.append(correct_list[i]['lastname'])
        person.append(correct_list[i]['firstname'])
        person.append(correct_list[i]['surname'])
        person.append(correct_list[i]['organization'])
        person.append(correct_list[i]['position'])
        person.append(correct_list[i]['phone'])
        person.append(correct_list[i]['email'])
        final_list.append(person)

pprint(final_list)

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(final_list)

  mport csv
import re


def read_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


def format_name(contacts_list):
    pattern_raw = r"^([А-ЯЁа-яё]+)(\s*)(\,?)([А-ЯЁа-яё]+)(\s*)(\,?)([А-ЯЁа-яё]*)(\,?)(\,?)(\,?)"
    pattern_new = r"\1\3\10\4\6\9\7\8"
    updated_contacts_list = []
    for entry in contacts_list:
        entry_string = ','.join(entry)
        edited_entry = re.sub(pattern_raw, pattern_new, entry_string)
        entry_list = edited_entry.split(",")
        updated_contacts_list.append(entry_list)
    return updated_contacts_list


def format_phone_number(contacts_list):
    pattern_raw = r"(\+7|8)(\s*)(\(*)(\d{3})(\)*)(\s*)(\-*)(\d{3})(\s*)(\-*)(\d{2})(\s*)(\-*)(\d{2})(\s*)(\(*)" \
                  r"(доб)*(\.*)(\s*)(\d+)*(\)*)"
    pattern_new = r"+7(\4)\8-\11-\14\15\17\18\20"
    updated_contacts_list = []
    for entry in contacts_list:
        entry_string = ','.join(entry)
        edited_entry = re.sub(pattern_raw, pattern_new, entry_string)
        entry_list = edited_entry.split(",")
        updated_contacts_list.append(entry_list)
    return updated_contacts_list


def duplicate_entries(contacts_list):
    for ent in contacts_list:
        if len(ent) > 7:
            del ent[-1]
    for i in contacts_list:
        for j in contacts_list:
            if i[0] == j[0] and i[1] == j[1] and i is not j:
                if i[2] == "":
                    i[2] = j[2]
                if i[3] == "":
                    i[3] = j[3]
                if i[4] == "":
                    i[4] = j[4]
                if i[5] == "":
                    i[5] = j[5]
                if i[6] == "":
                    i[6] = j[6]
    updated_contacts_list = []
    for entry in contacts_list:
        if entry not in updated_contacts_list:
            updated_contacts_list.append(entry)
    return updated_contacts_list


def write_file(contacts_list):
    with open("phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)


if __name__ == '__main__':
    phonebook = read_file('phonebook_raw.csv')
    phonebook = format_name(phonebook)
    phonebook = format_phone_number(phonebook)
    phonebook = duplicate_entries(phonebook)
    write_file(phonebook)    
