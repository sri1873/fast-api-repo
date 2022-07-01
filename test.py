import unittest

from fastapi.testclient import TestClient
from main import app

client= TestClient(app=app)

asset_data = {
    "laptop_id": "stng",
    "phone_id": "sg",
    "sim_number": 0,
    "benefits": "s",
    "email_id": "strig"
}

attendece_data = {
    "in_time": True
}

class TestMain(unittest.TestCase):
    def test_assests():
        response= client.post('/post_assets',json=asset_data)
        assert response.status_code==200


    def test_attendence():
        response= client.post('/add',json=attendece_data)
        assert response.status_code==200