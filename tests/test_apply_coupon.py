def test_apply_coupon_success(client):

    cart = {
        "cart": {
            "items": [
                {"product_id": 1, "quantity": 4, "price": 50}
            ]
        }
    }

    response = client.post(
        "/apply-coupon/1",
        json=cart
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "updated_cart" in data
    assert "final_price" in data["updated_cart"]

def test_coupon_not_applicable(client):

    cart = {
        "cart": {
            "items": [
                {"product_id": 5, "quantity": 1, "price": 20}
            ]
        }
    }

    response = client.post("/apply-coupon/1", json=cart)

    assert response.status_code == 400

def test_apply_coupon_empty_cart(client):

    cart = {"cart": {"items": []}}

    response = client.post("/apply-coupon/1", json=cart)

    assert response.status_code == 400