from flask import  Blueprint, request
from services.coupon_service import CouponService

blp_coupons = Blueprint('blp_products',__name__,url_prefix='/api/products')

class CouponController:

    @classmethod
    @blp_coupons.post("/coupons")
    def create_coupon(cls):
        req = request.json
        coupon_type = req["coupon_type"]
        min_cart_value = req["min_cart_value"]
        max_discount = req["max_discount"]
        coupon_expiry = req["coupon_expiry"]
        user_specific_flag = req["user_specific_flag"]
        valid_product_categories = req["valid_product_categories"]
        cart_size = req["cart_size"]
        return CouponService.create_coupon(coupon_type, min_cart_value, max_discount, coupon_expiry,
                                           user_specific_flag, valid_product_categories, cart_size)

    @classmethod
    @blp_coupons.get("/coupons")
    def fetch_coupon(cls):
        return CouponService.fetch_all_coupons()

    @classmethod
    @blp_coupons.get("/coupons/<int:coupon_id>")
    def fetch_coupon(cls, coupon_id):
        return CouponService.fetch_coupon(coupon_id)

    @classmethod
    @blp_coupons.delete("/coupons/<int:coupon_id>")
    def delete_coupon(cls, coupon_id):
        return CouponService.delete_coupon(coupon_id)

    @classmethod
    @blp_coupons.put("/coupons/<int:product_id>")
    def update_coupon(cls, coupon_id):
        req = request.json
        coupon_type = req["coupon_type"]
        min_cart_value = req["min_cart_value"]
        max_discount = req["max_discount"]
        coupon_expiry = req["coupon_expiry"]
        user_specific_flag = req["user_specific_flag"]
        valid_product_categories = req["valid_product_categories"]
        cart_size = req["cart_size"]
        return CouponService.update_coupon(coupon_id, coupon_type, min_cart_value, max_discount, coupon_expiry,
                                           user_specific_flag, valid_product_categories, cart_size)

    @classmethod
    @blp_coupons.post("/applicable-coupons")
    def create_coupon(cls):
        req = request.json
        min_cart_value = req["min_cart_value"]
        cart_size = req["cart_size"]
        max_discount = req["max_discount"]
        coupon_expiry = req["coupon_expiry"]
        user_specific_flag = req["user_specific_flag"]
        valid_product_categories = req["valid_product_categories"]
        return CouponService.applicable_coupons(min_cart_value, cart_size, max_discount, coupon_expiry,
                                             user_specific_flag, valid_product_categories)