from datetime import datetime
from extensions import db

class CouponsModel(db.Model):
    __tablename__ = "master_coupon_details"
    __table_args__= {"schema":"coupon_management"}

    coupon_id = db.Column(db.BigInteger, primary_key=True)
    coupon_type = db.Column(db.String)
    coupon_desc = db.Column(db.String)
    coupon_details  = db.Column(db.JSON)
    coupon_expiry  = db.Column(db.DateTime)
    active  = db.Column(db.Boolean)
    usage_limit = db.Column(db.Integer)
    user_limit = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
