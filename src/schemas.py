from pydantic import BaseModel
from datetime import date

class ExecutionBase(BaseModel):

    type: str
    price: int
    service_price: int
    message: str
    done_at: date
    date_recieve: date
    
class ExecutionCreate(ExecutionBase):

    pass

class Execution(ExecutionBase):

    id: int
    order_id: int
    worker_id: int

    class Config:
        orm_mode = True




class OrderBase(BaseModel):

    client_name: str
    client_phone: str
    garant: str
    arriving: date
    
class OrderCreate(OrderBase):

    pass

class Order(OrderBase):

    id: int
    product_id: int

    class Config:
        orm_mode = True




class WorkerBase(BaseModel):

    name: str
    role: str

class WorkerCreate(WorkerBase):

    pass

class Worker(WorkerBase):
    
    id: int
    execution: list[Execution] = []

    class Config:
        orm_mode = True



class ProductBase(BaseModel):
    
    product_name: str
    firm: str
    model: str
    review: str
    garant: str
    pic: str

class ProductCreate(ProductBase):
    
    pass

class Product(ProductBase):

    id: int
    order: list[Order] = []

    class Config:
        orm_mode = True