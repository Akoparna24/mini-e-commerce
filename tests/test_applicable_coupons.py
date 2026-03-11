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
        "/api/applicable-coupons",
        json=cart
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] is True
    assert isinstance(data["result"], list)

def test_applicable_coupons_empty_cart(client):

    cart = {"cart": {"items": []}}

    response = client.post(
        "/api/applicable-coupons",
        json=cart
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] is True
    assert data["result"] == []

def test_no_coupon_applicable(client):

    cart = {
        "cart": {
            "items": [
                {"product_id": 99, "quantity": 1, "price": 10}
            ]
        }
    }

    response = client.post("/api/applicable-coupons", json=cart)

    data = response.get_json()

    assert data["status"] is True
    assert data["result"] == []