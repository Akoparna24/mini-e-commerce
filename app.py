from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from extensions import db

from controllers.coupon_controller import blp_coupons

app = Flask(__name__)

# PostgreSQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:akoparnas24@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(blp_coupons)

if __name__ == "__main__":
    app.run(debug=True)