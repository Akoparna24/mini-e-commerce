from flask import  Blueprint, request
from services.coupon_service import CouponService

blp_coupons = Blueprint(
    "coupons",
    __name__,
    url_prefix="/api"
)

class CouponController:

    @classmethod
    @blp_coupons.post("/coupons")
    def create_coupon():
        req = request.json
        coupon_type = req["coupon_type"]
        coupon_title = req["coupon_title"]
        coupon_details = req["coupon_details"]
        coupon_expiry = req["coupon_expiry"]
        active = req["active"]
        usage_limit = req["usage_limit"]
        user_limit = req["user_limit"]
        return CouponService.create_coupon(coupon_type, coupon_title, coupon_details, coupon_expiry,
                                           active, usage_limit, user_limit)

    @blp_coupons.get("/coupons")
    def fetch_all_coupons():
        return CouponService.fetch_all_coupons()

    @blp_coupons.get("/coupons/<int:coupon_id>")
    def fetch_coupon(coupon_id):
        return CouponService.fetch_coupon(coupon_id)

    @blp_coupons.delete("/coupons/<int:coupon_id>")
    def delete_coupon(coupon_id):
        return CouponService.delete_coupon(coupon_id)

    @blp_coupons.put("/coupons/<int:coupon_id>")
    def update_coupon(coupon_id):
        req = request.json
        coupon_type = req["coupon_type"]
        coupon_title = req["coupon_title"]
        coupon_details = req["coupon_details"]
        coupon_expiry = req["coupon_expiry"]
        active = req["active"]
        usage_limit = req["usage_limit"]
        user_limit = req["user_limit"]
        return CouponService.update_coupon(coupon_id, coupon_type, coupon_title, coupon_details, coupon_expiry, active, usage_limit, user_limit)

    @blp_coupons.post("/applicable-coupons")
    def applicable_coupons():
        req = request.json
        cart = req["cart"]
        return CouponService.applicable_coupons(cart)

    @blp_coupons.post("/apply-coupon/<int:coupon_id>")
    def apply_coupon(coupon_id):
        req = request.json
        cart = req["cart"]
        return CouponService.apply_coupon(coupon_id, cart)
