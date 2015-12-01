import sys
sys.path.append('./../')

import bson
from feedbackbot.db_helper import Database
from feedbackbot.text_message import questions, info_messages, coupons
db = Database('messages')

question_no = 0
for question in questions:
	question.update({'question_no': question_no})
        if question['choice_type'] == 'image':
            question['image'] = bson.binary.Binary(open(question['image_path']).read())
        db.insert('questions', question)
	question_no += 1


coupon_no = 0
for coupon in coupons:
	coupon.update({'coupon_no': coupon_no})
        coupon['image'] = bson.binary.Binary(open(coupon['image_path']).read())
        db.insert('coupons', coupon)
	question_no += 1


for k, v in info_messages.iteritems():
	db.insert('info_messages', {k: v})
