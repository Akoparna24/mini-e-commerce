from flask import jsonify, make_response
from ecommerce.db_config import db
from repositories.coupon_repository import CouponRepo

class CouponService:

    @classmethod
    def create_coupon(cls, coupon_type, min_cart_value, max_discount, coupon_expiry, user_specific_flag,
                      valid_product_categories, cart_size):
        coupon_details = {
            "coupon_type": coupon_type,
            "min_cart_value": min_cart_value,
            "max_discount": max_discount,
            "coupon_expiry": coupon_expiry,
            "user_specific_flag": user_specific_flag,
            "valid_product_categories": valid_product_categories,
            "cart_size": cart_size
        }
        db.session.add(coupon_details)
        db.session.commit()

        return make_response(jsonify(message="Coupon created successfully", status=True), 200)

    @classmethod
    def fetch_coupon(cls, coupon_id):
        details = CouponRepo.fetch_coupon(coupon_id)
        coupon_details = {
            "coupon_type": details.coupon_type,
            "min_cart_value": details.min_cart_value,
            "max_discount": details.max_discount,
            "coupon_expiry": details.coupon_expiry,
            "user_specific_flag": details.user_specific_flag,
            "valid_product_categories": details.valid_product_categories,
            "cart_size": details.cart_size,
            "created_at": details.created_at,
            "updated_at": details.updated_at
        }
        return make_response(jsonify(coupon_details=coupon_details, status=True), 200)

    @classmethod
    def fetch_all_coupons(cls):
        details = CouponRepo.fetch_coupon()
        coupon_details = {
            "coupon_type": details.coupon_type,
            "min_cart_value": details.min_cart_value,
            "max_discount": details.max_discount,
            "coupon_expiry": details.coupon_expiry,
            "user_specific_flag": details.user_specific_flag,
            "valid_product_categories": details.valid_product_categories,
            "cart_size": details.cart_size,
            "created_at" : details.created_at,
            "updated_at": details.updated_at
        }
        return make_response(jsonify(coupon_details=coupon_details, status=True), 200)

    @classmethod
    def delete_coupon(cls, coupon_id):
        CouponRepo.delete_coupon(coupon_id)
        return make_response(jsonify(message="Coupon deleted successfully", status=True), 200)

    @classmethod
    def update_coupon(cls, coupon_id, coupon_type, min_cart_value, max_discount, coupon_expiry, user_specific_flag,
                      valid_product_categories, cart_size):
        CouponRepo.update_coupon(coupon_id, coupon_type, min_cart_value, max_discount, coupon_expiry, user_specific_flag,
                      valid_product_categories, cart_size)
        return make_response(jsonify(message="Coupon updated successfully", status=True), 200)
