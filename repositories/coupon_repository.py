from models.coupon_model import CouponsModel
from extensions import db

class CouponRepo:
    def __init__(self, coupon_type, coupon_desc, coupon_details, coupon_expiry, active, usage_limit, user_limit):
        self.coupon_type = coupon_type
        self.coupon_desc = coupon_desc
        self.coupon_details = coupon_details
        self.coupon_expiry = coupon_expiry
        self.active = active
        self.usage_limit = usage_limit
        self.user_limit = user_limit

    @classmethod
    def fetch_coupon(cls, coupon_id):
        return CouponsModel.query.get(coupon_id)

    @classmethod
    def fetch_all_coupons(cls):
        return CouponsModel.query.all()

    @classmethod
    def delete_coupon(cls, coupon_id):
        coupon = CouponsModel.query.get(coupon_id)
        db.session.delete(coupon)
        db.session.commit()

    @classmethod
    def update_coupon(cls, coupon_id, coupon_type, coupon_desc, coupon_details, coupon_expiry, active, usage_limit, user_limit):
        query = CouponsModel.query.get(coupon_id)
        query.update({
            "coupon_type": coupon_type,
            "coupon_desc": coupon_desc,
            "coupon_details": coupon_details,
            "coupon_expiry": coupon_expiry,
            "active": active,
            "usage_limit": usage_limit,
            "user_limit": user_limit
        })
        db.session.commit()
