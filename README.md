**Overview**
This project implements a RESTful API for managing and applying coupons in an e-commerce platform.
The system supports multiple coupon types and calculates applicable discounts based on cart contents.

**Supported coupon types:**
1. Cart-wise coupons – Apply discount on the entire cart if total exceeds a threshold.
2. Product-wise coupons – Apply discount on specific products.
3. BxGy coupons – Buy X items from a set of products and get Y items free from another set.

**Tech Stack**
1. Language: Python
2. Framework: Flask
3. Database: PostgreSQL

**Database Schema**

master_coupon_details table
| Field       | Type               | Description                          |
| ----------- | ------------------ | ------------------------------------ |
| coupon_id   | SERIAL PRIMARY KEY | Coupon ID                            |
| coupon_type | VARCHAR            | cart-wise / product-wise / bxgy      |
| coupon_desc | VARCHAR            | Coupon name                          |
| coupon_details | JSONB              | Coupon conditions and discount rules |
| coupon_expiry | TIMESTAMP          | Coupon expiration                    |
| active      | BOOLEAN            | Whether coupon is active             |
| usage_limit | INT                | Total allowed uses                   |
| user_limit  | INT                | Allowed uses per user                |
| created_at  | TIMESTAMP          | Creation time                        |
| updated_at  | TIMESTAMP          | Updation time                        |

Example coupon structure:
{
  "coupon_type": "bxgy",
  "coupon_desc": "Buy 1 get 1 free",
  "coupon_details": {
    "buy_products": [{"product_id": 1, "quantity": 1}],
    "get_products": [{"product_id": 1, "quantity": 2}],
    "repetition_limit": 3
  }
}

**API Endpoints**
1. POST /coupons - Create a new coupon.
2. GET /coupons - Retrieve all coupons.
3. GET /coupons/{id} - Retrieve a specific coupon.
4. PUT /coupons/{id} - Update coupon details.
5. DELETE /coupons/{id} - Remove a coupon.
6. POST /applicable-coupons - Returns all coupons applicable to a given cart.
   Example request:
   {
  "cart": {
    "items": [
      {"product_id": 1, "quantity": 2, "price": 50},
      {"product_id": 3, "quantity": 1, "price": 25}
    ]
  }
}
7. POST /apply-coupon/{id} - Applies a specific coupon to the cart and returns the updated cart with discounts.

**Implemented Coupon Cases**
1. Cart-wise
   a. Percentage discount on cart total
   b. Flat discount on cart total
   c. Minimum cart value threshold
   d. Maximum discount handled
2. Product-wise
   a. Discount applied to specific products
   b. Discount applied to multiple products
   c. Percentage and flat discounts supported
3. BxGy
   a. Buy products from a specified set
   b. Get products from another set
   c. Repetition limits supported
   Example:
   Buy 2 items from [X, Y]
   Get 1 item from [A, B] free

**Edge Cases Considered**
1. Cart related
   a. Empty cart
   b. Duplicate product entries
   c. Product quantity = 0
   d. Product price = 0
2. Coupon related
   a. Expired coupons
   b. Inactive coupons
   c. Coupon not found
   d. Invalid coupon ID
3. Cart-wise edge cases
   a. Cart total exactly equal to threshold
   b. Discount exceeding cart value
4. Product-wise edge cases
   a. Product not present in cart
   b. Product quantity below required minimum
5. BxGy edge cases
   a. Buy products partially present in cart
   b. Get products fewer than expected
   c. Repetition limit exceeded
   d. Free items exceeding available quantity

**Assumptions**
1. Only one coupon can be applied to a cart at a time.
2. Free products in BxGy coupons must already exist in the cart.
3. Discounts cannot exceed the product or cart total.
4. Coupon stacking is not supported.
5. Product prices are assumed to be valid and provided by the client.

**Limitations**
1. Category-based coupons are not implemented.
2. User-specific coupons are not implemented.
3. Coupon usage tracking per user is not implemented.
4. Coupon stacking is not supported.

**Future Improvements**
1. Support coupon stacking.
2. Add category-based coupons.
3. Add user-specific coupons.
4. Add coupon usage tracking.
5. Add priority rules when multiple coupons are applicable.

**Running the Project**
1. Clone the repository.
2. Install dependencies: pip install -r requirements.txt
3. Run the server: python app.py

**Testing**
You can test the APIs using:
1. Postman
2. Curl

**Bonus Features**
1. Coupon expiration dates
2. Unit tests
