# LaundryBot

##DataBase:
**Book**
| Column | Description |
| ------ | ----------- |
| _id | Unique identifier |
| time | time object |

**Users**
| Column | Description |
| ------ | ----------- |
| _id | Unique identifier |
| name | First name |
| surname | Last name |
| room | Room number |
| phone | Phone number |
| number_orders | Number of orders |
| telegram_id | Telegram ID |

**Visits**
| Column | Description |
| ------ | ----------- |
| _id | Unique identifier |
| telegram_id | Telegram ID |
| date | Date |
| full_name | Full name |
| room | Room number |
| time | Time slot |

**Book functions:**
* free_washers() - список объектов машинок, имеющих хотя бы один свободный слов времени.
* free_time(_id) - возвращает массив из семи элементов свободного времени у машинки с _id = _id (book)
[True, False, False, True, False, False, False]
* change_free_time(_id, time, bool) - меняет у машинки с _id временной промежуток с !bool на bool
* reset_washers() - каждые 18.00 меняет у всех машинок все время на True

**Users functions:**
* check_key(keys, values) - возвращает True, если есть пользователь с key[i] == value[i]
* add_info(name, surname, room, phone, id) - добавляет пользователю с name, surname, room id и phone
* give_user_number_orders(telegram_id) - возвращает количество стирок у пользователя
* change_number_orders(telegram_id, number) - меняет поле number_orders у пользователя с id на number
* reset_numbers_orders() - если завтра 1-ое число ставим количество orders_numbers всем на 4

**Visits functions:**
* add_string(telegram_id, date, full_name, room, time = “9.00-10.10”) - добавляет объект в базу данных
* del_string(telegram_id, date, time) - удаляет объект из базы данных
* fill_doc(low_date, high_date = now) - заполняет документ visit_users.excl посещений с low_date до high_date (по стандарту у high_date дата текущая)
