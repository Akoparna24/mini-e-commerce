import json

def test_applicable_coupons_success(client):

    cart = {
        "cart": {
            "items": [
                {"product_id": 1, "quantity": 4, "price": 50},
                {"product_id": 2, "quantity": 3, "price": 30}
            ]
        }
    }

    response = client.post(
        "/applicable-coupons",
        data=json.dumps(cart),
        content_type="application/json"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "applicable_coupons" in data
    assert isinstance(data["applicable_coupons"], list)

def test_applicable_coupons_empty_cart(client):

    cart = {"cart": {"items": []}}

    response = client.post(
        "/applicable-coupons",
        json=cart
    )

    assert response.status_code == 200
    assert response.get_json()["applicable_coupons"] == []

def test_no_coupon_applicable(client):

    cart = {
        "cart": {
            "items": [
                {"product_id": 99, "quantity": 1, "price": 10}
            ]
        }
    }

    response = client.post("/applicable-coupons", json=cart)

    data = response.get_json()

    assert data["applicable_coupons"] == []