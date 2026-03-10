from flask_smorest import Api

from controllers.coupon_controller import CouponController

def register_controllers(api: Api):
    api.register_blueprint(CouponController)
