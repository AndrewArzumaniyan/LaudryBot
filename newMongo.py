import datetime
import time
import pymongo
from copy import deepcopy


def connect_collection(str):
  db_client = pymongo.MongoClient("mongodb+srv://andrey:28122011@cluster0.i2aesum.mongodb.net/?retryWrites=true&w=majority")
  current_db = db_client['TeleBot']

  return current_db[str]

book = connect_collection('book')
users = connect_collection('users')
visits = connect_collection('visits')


#* Book
def free_washers():
  res = []
  for obj in book.find():
    time = list(obj['time'].values())
    if True in time:
      res.append(obj)
  
  return res

def free_time(_washer_id):
  res = []

  washer = book.find_one({"_id": _washer_id})
  for time in washer["time"].keys():
    if washer["time"][time]:
      res.append(time)

  return res

def change_free_time(_washer_id, time, boolValue):
  washer = book.find_one({ "_id": _washer_id })
  
  new_time_obj = deepcopy(washer["time"])
  new_time_obj[time] = boolValue

  book.update_one({ "id": _washer_id }, { "$set": new_time_obj })

# def reset_washers():
#   washers = book.find()

#   while True:
#     # Получаем текущее время
#     now = datetime.datetime.now()

#     # Если текущее время 18:00, меняем состояние всех машинок на True
#     if now.hour == 18 and now.minute == 0:
      

#     # Ждем до следующего дня
#     tomorrow = now + datetime.timedelta(days=1)
#     reset_time = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 18, 0, 0)
#     time.sleep((reset_time - now).total_seconds())


#* Users
def check_key(key, value):
  obj = users.find_one({key: value})
  if obj:
    return True
  return False

def add_info(name, surname, room, phone, telegram_id):
  filt = {"name": name, "surname": surname, "room": room}
  users.update_one(filt, { "$set": { "phone" : phone, "id": telegram_id } } )

def give_user_number_orders(telegram_id):
  return users.find_one({ "id": telegram_id })['number_orders']

def change_number_orders(telegram_id, number):
  users.update_one({ "id": telegram_id }, { "$set": { "number_orders" : number } } )


#* Visits
def add_string(telegram_id, date, full_name, room, time):
  visits.insert_one({ "id": telegram_id, "date": date, "full_name": full_name, "room": room, "time": time })

def del_string(telegram_id, date, time):
  visits.delete_one({ "id": telegram_id, "date": date, "time": time })



# def available_time():
#   available_time = []

#   book = connect_collection('book')
#   asd = book.find()
#   for obj in asd:
#     time = obj['time']
#     for key in time:
#       if not key in available_time:
#           if time[key] == True:
#             available_time.append(key)

#   return available_time

# def available_time_bool():
#   available_time = [False for i in range(8)]
#   tmp = []

#   book = connect_collection('book')
#   asd = book.find()
#   for obj in asd:
#     tmp.append(obj)
  
#   for i in range(len(tmp)):
#     time = list(tmp[i]['time'].values())
    
#     for j in range(len(time)):
#       if available_time[j]:
#         continue
#       if time[j]:
#         available_time[j] = True
  
#   return available_time
    


# async def auth_err(collection_name, key, message, answer):
#   collection = connect_collection(collection_name)
#   if not check_key(collection, key, message.text):
#     await message.answer(answer)
#     return True
#   return False

# def give_user(collection, id):
#   return collection.find_one({'id': id})

# def change_key(collection, filter, key, value):
#   collection.update_one(filter, { "$set": { key: value } })

# def change_key_book(collection, time, value):
#   document = collection.find()
#   tmp = []
#   for obj in document:
#     tmp.append(obj)
  
#   res = list(filter(lambda x: x["time"][time] != value, tmp))
  
#   if len(res):
#     cur_id = res[0]["_id"]
#     cur_filter = res[0]["time"]
#     res_filter = deepcopy(res[0]["time"])
#     res_filter[time] = value
#     collection.update_one({"time" : cur_filter}, { "$set": {"time": res_filter} })
#     return cur_id
#   return None