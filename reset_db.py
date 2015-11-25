from db_helper import Database

db = Database('messages')
db.delete('sent')
db.delete('recieved') 