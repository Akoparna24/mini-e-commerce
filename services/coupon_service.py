from datetime import datetime
from typing import Dict, List
from flask import jsonify, make_response
from extensions import db
from repositories.coupon_repository import CouponRepo
from constants import BXGY, CART_WISE, PRODUCT_WISE
from models.coupon_model import CouponsModel

class CouponService:

    @classmethod
    def create_coupon(cls, coupon_type, coupon_desc, coupon_details, coupon_expiry, active, usage_limit, user_limit):
        try:
            # coupon_details = {
            #     "coupon_type": coupon_type,
            #     "coupon_desc": coupon_desc,
            #     "coupon_details": coupon_details,
            #     "coupon_expiry": coupon_expiry,
            #     "active": active,
            #     "usage_limit": usage_limit,
            #     "user_limit": user_limit
            # }
            coupon_details = CouponsModel(
                coupon_type=coupon_type,
                coupon_desc=coupon_desc,
                coupon_details=coupon_details,
                coupon_expiry=coupon_expiry,
                active=active,
                usage_limit=usage_limit,
                user_limit=user_limit
            )
            db.session.add(coupon_details)
            db.session.commit()

            return make_response(jsonify(message="Coupon created successfully", status=True), 200)

        except Exception as e:
            print(f"Exception: {e}")
            db.session.rollback()
            return make_response(jsonify(message="Coupon not created", status=False), 500)

    @classmethod
    def fetch_coupon(cls, coupon_id):
        try:
            details = CouponRepo.fetch_coupon(coupon_id)
            coupon_details = {
                "coupon_id": details.coupon_id,
                "coupon_type": details.coupon_type,
                "coupon_desc": details.coupon_desc,
                "coupon_details": details.coupon_details,
                "coupon_expiry": details.coupon_expiry,
                "active": details.active,
                "usage_limit": details.usage_limit,
                "user_limit": details.user_limit,
                "created_at": details.created_at,
                "updated_at": details.updated_at
            }
            return make_response(jsonify(coupon_details=coupon_details, status=True), 200)

        except Exception as e:
            return make_response(jsonify(message="Coupon Not Found", status=False), 500)

    @classmethod
    def fetch_all_coupons(cls):
        all_coupon_details = list()
        all_coupons = CouponRepo.fetch_all_coupons()
        for coupon in all_coupons:
            coupon_details = {
                "coupon_id": coupon.coupon_id,
                "coupon_type": coupon.coupon_type,
                "coupon_desc": coupon.coupon_desc,
                "coupon_details": coupon.coupon_details,
                "coupon_expiry": coupon.coupon_expiry,
                "active": coupon.active,
                "usage_limit": coupon.usage_limit,
                "user_limit": coupon.user_limit,
                "created_at" : coupon.created_at,
                "updated_at": coupon.updated_at
            }
            all_coupon_details.append(coupon_details)
        return make_response(jsonify(coupon_details=all_coupon_details, status=True), 200)

    @classmethod
    def delete_coupon(cls, coupon_id):
        try:
            CouponRepo.delete_coupon(coupon_id)
            return make_response(jsonify(message="Coupon deleted successfully", status=True), 200)

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify(message="Coupon Not Deleted", status=False), 500)

    @classmethod
    def update_coupon(cls, coupon_id, coupon_type, coupon_desc, coupon_details, coupon_expiry, active, usage_limit, user_limit):
        try:
            CouponRepo.update_coupon(coupon_id, coupon_type, coupon_desc, coupon_details, coupon_expiry, active, usage_limit, user_limit)
            return make_response(jsonify(message="Coupon updated successfully", status=True), 200)

        except Exception as e:
            print(f"Exception: {e}")
            db.session.rollback()
            return make_response(jsonify(message="Coupon Not Updated", status=False), 500)

    @classmethod
    def applicable_coupons(cls, cart: Dict):
        """
            Calculate all applicable coupons for a given cart.
            Let us assume cart parameters as: { "items": [{"product_id": int, "quantity": int, "price": float}, ...] }
        """
        try:
            coupons = CouponRepo.fetch_all_coupons()
            applicable_coupons = []
            cart_total = sum(item["quantity"] * item["price"] for item in cart["items"])
            current_time = datetime.now()
            for coupon in coupons:
                # Skip inactive or expired coupons
                if not coupon.active:
                    continue
                expiry = coupon.coupon_expiry
                if expiry and current_time > expiry:
                    continue
                discount = 0
                coupon_type = coupon.coupon_type
                details = coupon.coupon_details

                if coupon_type == CART_WISE:
                    threshold = details["threshold"]
                    if cart_total >= threshold:
                        amount = details["discount"]
                        dtype = details["discount_type"]
                        if dtype == "percentage":
                            discount = cart_total * amount / 100
                        else:
                            discount = amount

                elif coupon_type == PRODUCT_WISE:
                    product_ids = details["product_ids"]
                    amount = details["discount"]
                    dtype = details["discount_type"]
                    for item in cart["items"]:
                        if item["product_id"] in product_ids:
                            if dtype == "percentage":
                                discount += item["price"] * item["quantity"] * amount / 100
                            else:
                                # flat discount per item
                                discount += min(amount * item["quantity"], item["price"] * item["quantity"])

                elif coupon_type == BXGY:
                    buy_products = details["buy_products"]
                    get_products = details["get_products"]
                    repetition_limit = details["repetition_limit"]

                    applications = repetition_limit
                    for bp in buy_products:
                        cart_item = next((i for i in cart["items"] if i["product_id"] == bp["product_id"]), None)
                        if not cart_item or cart_item["quantity"] < bp["quantity"]:
                            applications = 0
                            break
                        possible = cart_item["quantity"] // bp["quantity"]
                        applications = min(applications, possible)

                    if applications > 0:
                        for gp in get_products:
                            cart_item = next((i for i in cart["items"] if i["product_id"] == gp["product_id"]), None)
                            if cart_item:
                                free_qty = gp["quantity"] * applications
                                discount_qty = min(free_qty, cart_item["quantity"])
                                discount += discount_qty * cart_item["price"]

                if discount > 0:
                    if len(applicable_coupons) > 0:
                        index = next((i for i, c in enumerate(applicable_coupons) if c["coupon_type"] == coupon_type), None)

                        if index is not None:
                            if applicable_coupons[index]['discount']<discount:
                                applicable_coupons[index] = {"coupon_id": coupon.coupon_id, "coupon_type": coupon_type, "discount": round(discount, 2)}
                        else:
                            applicable_coupons.append({
                                "coupon_id": coupon.coupon_id,
                                "coupon_type": coupon_type,
                                "discount": round(discount, 2)
                            })
                    else:
                        applicable_coupons.append({
                            "coupon_id": coupon.coupon_id,
                            "coupon_type": coupon_type,
                            "discount": round(discount, 2)
                        })

            return make_response(jsonify(result=applicable_coupons, status=True), 200)

        except Exception as e:
            print(f"Exception: {e}")
            return make_response(jsonify(message="Cart not eligible for applying coupons", status=False), 500)

    @classmethod
    def apply_coupon(cls, coupon_id, cart):
        try:
            items = cart.get("items", [])

            if not cart or "cart" not in cart:
                return jsonify({"status": False, "message": "Invalid cart"}), 400

            if not items:
                return jsonify({"error": "Cart is empty"}), 500

            coupon = CouponRepo.fetch_coupon(coupon_id)

            if not coupon:
                return jsonify({"error": "Coupon not found"}), 404

            if coupon.coupon_expiry and coupon.coupon_expiry < datetime.now():
                return jsonify({"error": "Coupon expired"}), 500

            details = coupon.coupon_details
            coupon_type = coupon.coupon_type

            total_discount = 0

            for item in items:
                item["discount"] = 0

            # CART WISE
            if coupon_type == CART_WISE:

                threshold = details.get("threshold")
                discount = details.get("discount")
                discount_type = details.get("discount_type")

                cart_total = sum(i["price"] * i["quantity"] for i in items)

                if cart_total < threshold:
                    return jsonify({"error": "Coupon not applicable"}), 400

                if discount_type == "percentage":
                    total_discount = cart_total * discount / 100
                else:
                    total_discount = discount

            # PRODUCT WISE
            elif coupon_type == PRODUCT_WISE:

                product_ids = details.get("product_ids", [])
                discount = details.get("discount")
                discount_type = details.get("discount_type")

                for item in items:

                    if item["product_id"] in product_ids:

                        item_total = item["price"] * item["quantity"]

                        if discount_type == "percentage":
                            item_discount = item_total * discount / 100
                        else:
                            item_discount = discount

                        item["discount"] = item_discount
                        total_discount += item_discount

            # BXGY
            elif coupon_type == BXGY:

                buy_products = details.get("buy_products", [])
                get_products = details.get("get_products", [])
                repetition_limit = details.get("repetition_limit", 1)

                buy_product_id = buy_products[0]["product_id"]
                buy_qty = buy_products[0]["quantity"]

                get_product_id = get_products[0]["product_id"]
                get_qty = get_products[0]["quantity"]

                cart_map = {i["product_id"]: i for i in items}

                if buy_product_id not in cart_map:
                    return jsonify({"error": "Coupon not applicable"}), 400

                buy_item = cart_map[buy_product_id]

                repetitions = min(buy_item["quantity"] // buy_qty, repetition_limit)

                if repetitions == 0:
                    return jsonify({"error": "Coupon not applicable"}), 400

                if get_product_id in cart_map:
                    get_item = cart_map[get_product_id]

                    free_items = min(get_item["quantity"], repetitions * get_qty)

                    discount = free_items * get_item["price"]

                    get_item["discount"] = discount
                    total_discount += discount

            total_price = sum(i["price"] * i["quantity"] for i in items)

            final_price = total_price - total_discount

            return make_response(jsonify(result={
                "updated_cart": {
                    "items": items,
                    "total_price": total_price,
                    "total_discount": total_discount,
                    "final_price": final_price
                }
            }, status=True),200)

        except Exception as e:
            print(f"Exception: {e}")
            return make_response(jsonify(message="Could not apply coupon", status=False), 500)
