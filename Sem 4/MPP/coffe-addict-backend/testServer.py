import pytest
from fastapi.testclient import TestClient
from server import app, coffee_shops, drinks
client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Coffee Addict API"}

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_coffee_shops():
    response = client.get("/coffee-shops?latitude=46.77&longitude=23.59")
    assert response.status_code == 200
    assert "coffee_shops" in response.json()
    
    response = client.get("/coffee-shops?latitude=46.77&longitude=23.59&sort_by=location")
    assert response.status_code == 200
    
    response = client.get("/coffee-shops?latitude=46.77&longitude=23.59&sort_by=rating&sort_order=desc")
    assert response.status_code == 200
    
    response = client.get("/coffee-shops?latitude=46.77&longitude=23.59&Open=true")
    assert response.status_code == 200
    
    response = client.get("/coffee-shops?latitude=91&longitude=23.59")
    assert response.status_code == 400
    
    response = client.get("/coffee-shops?latitude=46.77&longitude=23.59&sort_by=invalid")
    assert response.status_code == 400
    
    response = client.get("/coffee-shops?latitude=46.77&longitude=23.59&min_rating=6")
    assert response.status_code == 400

def test_get_coffee_shop():
    valid_id = coffee_shops[0]["public_id"]
    response = client.get(f"/coffee-shops/{valid_id}")
    assert response.status_code == 200
    assert "coffee_shops" in response.json()
    
    response = client.get("/coffee-shops/invalid-id")
    assert response.status_code == 404

def test_get_coffee_shop_drinks():
    valid_id = coffee_shops[0]["public_id"]
    response = client.get(f"/coffee-shops/{valid_id}/drinks")
    assert response.status_code == 200
    assert "drinks" in response.json()
    
    response = client.get("/coffee-shops/invalid-id/drinks")
    assert response.status_code == 404

def test_create_coffee_shop_drink():
    valid_id = coffee_shops[0]["public_id"]
    drink_data = {
        "name": "Test Drink",
        "description": "Test Description",
        "price": "5.00",
        "image": "https://example.com/image.jpg",
        "sales": 100,
        "popularity": 80
    }
    
    response = client.post(f"/coffee-shops/{valid_id}/drinks", json=drink_data)
    assert response.status_code == 200
    assert "drink" in response.json()
    assert response.json()["drink"]["name"] == "Test Drink"
    
    response = client.post(f"/coffee-shops/{valid_id}/drinks", json={"name": "Test"})
    assert response.status_code == 400
    
    invalid_data = drink_data.copy()
    invalid_data["name"] = 123
    response = client.post(f"/coffee-shops/{valid_id}/drinks", json=invalid_data)
    assert response.status_code == 400

def test_update_coffee_shop_drink():
    valid_shop_id = coffee_shops[0]["public_id"]
    valid_drink_id = drinks[0]["id"]
    drink_data = {
        "name": "Enspreso",
        "description": "Test Description",
        "price": "2.00",
        "image": "https://example.com/updated.jpg",
        "sales": 150,
        "popularity": 90
    }
    
    response = client.put(f"/coffee-shops/{valid_shop_id}/drinks/{valid_drink_id}", json=drink_data)
    assert response.status_code == 200
    assert response.json()["drink"]["name"] == "Enspreso"
    
    response = client.put(f"/coffee-shops/{valid_shop_id}/drinks/9999", json=drink_data)
    assert response.status_code == 404

def test_delete_coffee_shop_drink():
    valid_shop_id = coffee_shops[0]["public_id"]
    
    drink_data = {
        "name": "To Delete",
        "description": "Will be deleted",
        "price": "5.00",
        "image": "https://example.com/delete.jpg",
        "sales": 100,
        "popularity": 80
    }
    create_response = client.post(f"/coffee-shops/{valid_shop_id}/drinks", json=drink_data)
    drink_id = create_response.json()["drink"]["id"]
    
    response = client.delete(f"/coffee-shops/{valid_shop_id}/drinks/{drink_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Drink deleted"}
    
    response = client.delete(f"/coffee-shops/{valid_shop_id}/drinks/9999")
    assert response.status_code == 404


if __name__ == "__main__":
    pytest.main()