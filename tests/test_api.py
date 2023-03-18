from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app, get_db
from src.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite_base.db"  # Тестовая БД

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)  # Удалем таблицы из БД
Base.metadata.create_all(bind=engine)  # Создаем таблицы в БД


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db  # Делаем подмену

client = TestClient(app)  # создаем тестовый клиент к нашему приложению

def test_create_product():
    response = client.post(
        "/products/",
        json={"product_name": "test", "firm": "testfirm", "model" : "newModel", "review": "some review", "garant": "yes", "pic": "pic.png"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["product_name"] == "test"

def test_create_exist_product():
    response = client.post(
        "/products/",
        json={"product_name": "test", "firm": "testfirm", "model" : "newModel", "review": "some review", "garant": "yes", "pic": "pic.png"}
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Такой продукт уже есть"

def test_read_products():
    response = client.get("/products/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["product_name"] == "test"

def test_get_product_by_id():
    response = client.get("/products/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["product_name"] == "test"

def test_product_not_found():
    response = client.get("/products/2")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Такого продукта нет"



def test_create_worker():
    response = client.post(
        "/workers/",
        json={"name": "Work", "role": "clown"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Work"

def test_read_workers():
    response = client.get("/workers/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["name"] == "Work"

def test_get_worker_by_id():
    response = client.get("/workers/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Work"

def test_worker_not_found():
    response = client.get("/workers/2")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Такого рабочего нет"


def test_create_order():
    response = client.post(
        "/orders/1/",
        json={"client_name": "Tested", "client_phone": "000", "garant": "yes", "arriving": "1995-10-11"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["client_name"] == "Tested"
    assert data["client_phone"] == "000"
    assert data["garant"] == "yes"
    assert data["arriving"] == "1995-10-11"

def test_get_order_by_id():
    response = client.get("/orders/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["client_name"] == "Tested"

def test_order_not_found():
    response = client.get("/orders/2")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Такого заказа нет"

def test_read_orders():
    response = client.get("/orders/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["client_name"] == "Tested"


def test_create_execution():
    response = client.post(
        "/executions/1/1",
        json={"type": "test type", "price": 1000, "service_price": 1150, "message": "Drink", "done_at": "1991-12-12", "date_recieve": "1992-01-01"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["type"] == "test type"
    assert data["price"] == 1000
    assert data["service_price"] == 1150
    assert data["message"] == "Drink"
    assert data["done_at"] == "1991-12-12"
    assert data["date_recieve"] == "1992-01-01"

def test_get_execution_by_id():
    response = client.get("/executions/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["type"] == "test type"

def test_execution_not_found():
    response = client.get("/executions/2")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Такого выполнения заказа нет"

def test_read_executions():
    response = client.get("/executions/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["type"] == "test type"
