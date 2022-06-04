# #main.py
import re
import  string
from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv

# def split_FIO(contact_list, contact_list1=[]):
def parser(contacts_list):
    contact_list1 = []
    for record in contacts_list[0:]:
        contact_list_row = []
        FIO = ((record[0].strip() + ' '+ record[1].strip() + ' ' + record[2].strip()).strip()).split(' ') 
        for i in range(3):
            if i < len(FIO):
               contact_list_row.append(FIO[i])
            else:
               contact_list_row.append('')
        FI = contact_list_row[0] + contact_list_row[1] #ключ- фамилия и имя
        FI2 = contact_list_row[2] # отчество
        contact_list_row.append(record[3])
        contact_list_row.append(record[4])
        pattern = r'(\+)?(7|8)\s?\(?(\d{3})\)?\s?\-?(\d{3})\-?(\d{2})\-?(\d{2})\s?\(?(доб\.)?\s?(\d{4})?\)?'
        result = re.sub(pattern, r"+\2(\3)\4-\5-\6 \7\8", record[5])
        contact_list_row.append(result.strip())
        contact_list_row.append(record[6])
        if_must_ap = True
        if record[0] == 'lastname':
            contact_list1.append(contact_list_row)
            if_must_ap = False            
        else:
            for value in contact_list1:
                if (value[0] + value[1]) == FI:
                    if value[2] != FI2:
                        value[2] += FI2
                    if value[3] != record[3]:
                        value[3] += record[3]
                    if value[4] != record[4]:
                        value[4] += record[4]
                    if value[5] != result:
                        value[5] += ' '+ result
                        value[5] = value[5].strip()
                    if value[6] != record[6]:
                        value[6] += record[6]
                    if_must_ap = False
                    break
        if if_must_ap:
            contact_list1.append(contact_list_row)

    contacts_list = contact_list1
    print(contact_list1)
    print(contacts_list)
    return(contacts_list)        


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding="utf-8") as f:
      rows = csv.reader(f, delimiter=",")
      contacts_list = list(rows)

    contact_list1 = []
    for record in contacts_list[0:]:
        contact_list_row = []
        FIO = ((record[0].strip() + ' '+ record[1].strip() + ' ' + record[2].strip()).strip()).split(' ') 
        for i in range(3):
            if i < len(FIO):
               contact_list_row.append(FIO[i])
            else:
               contact_list_row.append('')
        FI = contact_list_row[0] + contact_list_row[1] #ключ- фамилия и имя
        FI2 = contact_list_row[2] # отчество
        contact_list_row.append(record[3])
        contact_list_row.append(record[4])
        pattern = r'(\+)?(7|8)\s?\(?(\d{3})\)?\s?\-?(\d{3})\-?(\d{2})\-?(\d{2})\s?\(?(доб\.)?\s?(\d{4})?\)?'
        result = re.sub(pattern, r"+\2(\3)\4-\5-\6 \7\8", record[5])
        contact_list_row.append(result.strip())
        contact_list_row.append(record[6])
        if_must_ap = True
        if record[0] == 'lastname':
            contact_list1.append(contact_list_row)
            if_must_ap = False            
        else:
            for value in contact_list1:
                if (value[0] + value[1]) == FI:
                    if value[2] != FI2:
                        value[2] += FI2
                    if value[3] != record[3]:
                        value[3] += record[3]
                    if value[4] != record[4]:
                        value[4] += record[4]
                    if value[5] != result:
                        value[5] += ' '+ result
                        value[5] = value[5].strip()
                    if value[6] != record[6]:
                        value[6] += record[6]
                    if_must_ap = False
                    break
        if if_must_ap:
            contact_list1.append(contact_list_row)
    
    print(contact_list1)

    with open("phonebook.csv", "w", newline='') as f:
      datawriter = csv.writer(f, delimiter=',')
      datawriter.writerows(contact_list1)