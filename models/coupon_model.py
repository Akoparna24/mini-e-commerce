from datetime import datetime
from ecommerce.db_config import db


class CouponsModel(db.Model):
    __table_name__ = "coupon_details"
    __table_args__= {"schema":"coupons_schema"}

    coupon_id = db.Column(db.Integer, primary_key=True)
    coupon_type = db.Column(db.String)
    min_cart_value = db.Column(db.Integer)
    max_discount  = db.Column(db.Integer)
    coupon_expiry  = db.Column(db.DateTime)
    user_specific_flag  = db.Column(db.String)
    valid_product_categories = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())