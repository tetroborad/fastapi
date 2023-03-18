from sqlalchemy.orm import Session

from src import models, schemas

def create_product(db:Session, product: schemas.ProductCreate):

    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def create_worker(db:Session, worker: schemas.WorkerCreate):

    db_worker = models.Worker(**worker.dict())
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker

def create_order(db:Session, order: schemas.OrderCreate, product_id: int):

    db_order = models.Order(**order.dict(), product_id=product_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def create_execution(db:Session, execution: schemas.ExecutionCreate, order_id: int, worker_id: int):

    db_execution = models.Execution(**execution.dict(), order_id=order_id, worker_id=worker_id)
    db.add(db_execution)
    db.commit()
    db.refresh(db_execution)
    return db_execution



def get_product_by_id(db: Session, product_id: int):

    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_worker_by_id(db: Session, worker_id: int):

    return db.query(models.Worker).filter(models.Worker.id == worker_id).first()

def get_order_by_id(db: Session, order_id: int):

    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_execution_by_id(db: Session, execution_id: int):

    return db.query(models.Execution).filter(models.Execution.id == execution_id).first()



def get_product_by_name(db: Session, product_name: str):
    return db.query(models.Product).filter(models.Product.product_name == product_name).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Product).offset(skip).limit(limit).all()

def get_workers(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Worker).offset(skip).limit(limit).all()

def get_orders(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Order).offset(skip).limit(limit).all()

def get_executions(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Execution).offset(skip).limit(limit).all()
