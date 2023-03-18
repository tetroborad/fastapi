from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    """
    Задаем зависимость к БД. При каждом запросе будет создаваться новое
    подключение.
    """
    db = SessionLocal()  # pragma: no cover
    try:  # pragma: no cover 
        yield db  # pragma: no cover
    finally:  # pragma: no cover
        db.close()  # pragma: no cover

@app.get("/products/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product_by_id(product_id: int, db: Session = Depends(get_db)):

    db_product = crud.get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Такого продукта нет")
    return db_product

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):

    db_product = crud.get_product_by_name(db, product_name=product.product_name)
    if db_product:
        raise HTTPException(status_code=400, detail="Такой продукт уже есть")
    return crud.create_product(db=db, product=product)




@app.get("/workers/", response_model=list[schemas.Worker])
def read_workers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    workers = crud.get_workers(db, skip=skip, limit=limit)
    return workers

@app.get("/workers/{worker_id}", response_model=schemas.Worker)
def read_worker_by_id(worker_id: int, db: Session = Depends(get_db)):

    db_worker = crud.get_worker_by_id(db, worker_id=worker_id)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Такого рабочего нет")
    return db_worker

@app.post("/workers/", response_model=schemas.Worker)
def create_worker(worker: schemas.WorkerCreate, db: Session = Depends(get_db)):

    return crud.create_worker(db=db, worker=worker)




@app.post("/orders/{product_id}", response_model=schemas.Order)
def create_order(
    product_id: int, order: schemas.OrderCreate, db: Session = Depends(get_db)
):
    return crud.create_order(db=db, order=order, product_id=product_id)

@app.get("/orders/{order_id}", response_model=schemas.Order)
def read_product_by_id(order_id: int, db: Session = Depends(get_db)):

    db_order = crud.get_order_by_id(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Такого заказа нет")
    return db_order

@app.get("/orders/", response_model=list[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders



@app.post("/executions/{order_id}/{worker_id}", response_model=schemas.Execution)
def create_execution(
    worker_id: int, order_id: int, execution: schemas.ExecutionCreate, db: Session = Depends(get_db)
):
    return crud.create_execution(db=db, execution=execution, worker_id=worker_id, order_id=order_id)

@app.get("/executions/{execution_id}", response_model=schemas.Execution)
def read_execution_by_id(execution_id: int, db: Session = Depends(get_db)):

    db_execution = crud.get_execution_by_id(db, execution_id=execution_id)
    if db_execution is None:
        raise HTTPException(status_code=404, detail="Такого выполнения заказа нет")
    return db_execution

@app.get("/executions/", response_model=list[schemas.Execution])
def read_executions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    executions = crud.get_executions(db, skip=skip, limit=limit)
    return executions



