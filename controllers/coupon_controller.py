from flask import  Blueprint, request


blp_coupons = Blueprint('blp_products',__name__,url_prefix='/api/products')

class CouponController:

    @classmethod
    @blp_coupons.post("/create-coupon")
    def create_coupon(cls):
        req = request.json
        coupon_type = req["coupon_type"]
        min_cart_value = req["min_cart_value"]
        max_discount = req["max_discount"]
        coupon_expiry = req["coupon_expiry"]
        user_specific_flag = req["user_specific_flag"]
        valid_product_categories = req["valid_product_categories"]
        return CouponService.create_coupon(coupon_type, min_cart_value, max_discount, coupon_expiry,
                                             user_specific_flag, valid_product_categories)

    @classmethod
    @blp_coupons.get("/fetch-coupons")
    def fetch_coupon(cls):
        return CouponService.fetch_coupons()

    @classmethod
    @blp_coupons.get("/fetch-coupon/<int:coupon_id>")
    def fetch_coupon(cls, coupon_id):
        return CouponService.fetch_coupon(coupon_id)

    @classmethod
    @blp_coupons.delete("/delete-coupon/<int:coupon_id>")
    def delete_coupon(cls, coupon_id):
        return CouponService.delete_coupon(coupon_id)

    @classmethod
    @blp_coupons.put("/update-product/<int:product_id>")
    def update_coupon(cls, coupon_id):
        req = request.json
        coupon_type = req["coupon_type"]
        min_cart_value = req["min_cart_value"]
        max_discount = req["max_discount"]
        coupon_expiry = req["coupon_expiry"]
        user_specific_flag = req["user_specific_flag"]
        valid_product_categories = req["valid_product_categories"]
        return CouponService.create_coupon(coupon_type, min_cart_value, max_discount, coupon_expiry,
                                             user_specific_flag, valid_product_categories)