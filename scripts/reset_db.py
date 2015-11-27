import sys
sys.path.append('./../')

from feedbackbot.db_helper import Database

db = Database('messages')
db.delete('sent')
db.delete('received')

# db.delete('questions')
# db.delete('message_info')