
class Coupon:
	def __init__(self, db):
		self.db = db

	def get_coupon(self, coupon_no):
		coupon_data = self.db.find('coupons', {'coupon_no': coupon_no})
		try:
			coupon_data = coupon_data[0]['image']
		except Exception:
			coupon_data = None
		return coupon_data


