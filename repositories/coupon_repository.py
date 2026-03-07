from ecommerce.db_config import db
from product_management.models.product_model import ProductsModel

class CouponRepo:
    def __init__(self, coupon_type, min_cart_value, max_discount, coupon_expiry, user_specific_flag,
                      valid_product_categories):
        self.coupon_type = coupon_type
        self.min_cart_value = min_cart_value
        self.max_discount = max_discount
        self.coupon_expiry = coupon_expiry
        self.user_specific_flag = user_specific_flag
        self.valid_product_categories = valid_product_categories

    @classmethod
    def fetch_coupon(cls, coupon_id):
        return ProductsModel.query.get(coupon_id)

    @classmethod
    def fetch_all_coupons(cls):
        return ProductsModel.query.all()

    @classmethod
    def delete_coupon(cls, coupon_id):
        coupon = ProductsModel.query.get(coupon_id)
        db.session.delete(coupon)
        db.session.commit()

    @classmethod
    def update_coupon(cls, coupon_id, coupon_type, min_cart_value, max_discount, coupon_expiry, user_specific_flag,
                      valid_product_categories):
        query = ProductsModel.query.get(coupon_id)
        query.update({
            "coupon_type": coupon_type,
            "min_cart_value": min_cart_value,
            "max_discount": max_discount,
            "coupon_expiry": coupon_expiry,
            "user_specific_flag": user_specific_flag,
            "valid_product_categories": valid_product_categories
        })
        db.session.commit()
