from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()

class BaseModel(Base):
    """
    Абстартный базовый класс, где описаны все поля и методы по умолчанию
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)

    def __repr__(self):
        return f"<{type(self).__name__}(id={self.id})>"  # pragma: no cover
    
class Product(BaseModel):
    __tablename__ = "products"

    product_name = Column(String)
    firm = Column(String)
    model = Column(String)
    review = Column(String)
    garant = Column(String)
    pic = Column(String)

    order = relationship("Order", back_populates="product")


class Worker(BaseModel):
    __tablename__ = "workers"

    name = Column(String)
    role = Column(String)
    
    execution = relationship("Execution", back_populates="worker")

class Order(BaseModel):
    __tablename__ = "orders"

    client_name = Column(String)
    client_phone = Column(String)
    garant = Column(String)
    arriving = Column(DateTime)
    product_id = Column(Integer, ForeignKey("products.id"))

    product = relationship("Product", back_populates="order")
    execution = relationship("Execution", back_populates="order")

class Execution(BaseModel):
    __tablename__ = "executions"


    type = Column(String)
    price = Column(Integer)
    service_price = Column(Integer)
    message = Column(String)
    done_at = Column(DateTime)
    date_recieve = Column(DateTime)
    order_id = Column(Integer, ForeignKey("orders.id"))
    worker_id = Column(Integer, ForeignKey("workers.id"))

    order = relationship("Order", back_populates="execution")
    worker = relationship("Worker", back_populates="execution")



