from fastapi.testclient import TestClient
from .main import app
import requests
from pydantic import BaseModel

client = TestClient(app)
class City(BaseModel):
    name: str 
    timezone: str
db = []
def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'key' : 'value'}

def test_get_cities():
    response = client.get("/cities")
    assert response.status_code == 200
    for city in db:
        r = requests.get(f'http://worldtimeapi.org/api/timezone/{city["timezone"]}')
        current_time = r.json()['datetime']
        assert response.json() == {'name' : city['name'], 'timezone' : city['timezone'], 'current_time' : current_time}

def test_get_city(city_id: int):
    response = client.get("/cities/{city_id}")
    assert response.status_code == 200
    city = db[city_id - 1]
    r = requests.get(f'http://worldtimeapi.org/api/timezone/{city["timezone"]}')
    current_time = r.json()['datetime']
    assert response.json() == {'name' : city['name'], 'timezone' : city['timezone'], 'current_time' : current_time}

def test_create_city(city: City):
    response = client.get("/cities")
    assert response.status_code == 200
    db.append(city.dict())
    assert response.json() == db[-1]

def test_delete_city(city_id: int):
    response = client.get("/cities/{city_id}")
    assert response.status_code == 200
    db.pop(city_id-1)
    assert response.json() == {}