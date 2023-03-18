"""empty message

Revision ID: first_data
Revises: 3b887b8f502d
Create Date: 2023-03-15 00:58:20.621416

"""
from alembic import op
from sqlalchemy import orm
from datetime import datetime

from src.models import Worker, Product, Execution, Order


# revision identifiers, used by Alembic.
revision = 'first_data'
down_revision = '3b887b8f502d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)


    product1 = Product(product_name='Product1', firm='TestFirm1', model='Test model 1', review='Какие-то технические характеристики', garant='2 года', pic='test.png')
    product2 = Product(product_name='Product2', firm='TestFirm2', model='Test model 2', review='Какие-то технические характеристики', garant='3 года', pic='test1.png')

    session.add_all([product1, product2])
    session.flush()

    worker1 = Worker(name='Cornelius', role='Carpenter')
    worker2 = Worker(name='Rupert', role='Cleaner')

    session.add_all([worker1, worker2])
    session.flush()

    order1 = Order(client_name='client 1', client_phone='111-111', garant='Yes', arriving=datetime(2019, 1, 25, 10, 10), product_id = product2.id)
    order2 = Order(client_name='client 2', client_phone='789-123', garant='No', arriving=datetime(2020, 1, 25, 10, 10), product_id = product1.id)
    order3 = Order(client_name='client 3', client_phone='101-456', garant='Yes', arriving=datetime(2021, 1, 25, 10, 10), product_id = product2.id)
    order4 = Order(client_name='client 4', client_phone='321-123', garant='No', arriving=datetime(2022, 1, 25, 10, 10), product_id = product1.id)

    session.add_all([order1, order2, order3, order4])
    session.commit()

    exec1 = Execution(type='type 1', price=1000, service_price=2000, message='done', done_at=datetime(2025, 2, 25, 10, 10), date_recieve=datetime(2025, 3, 1, 10, 10), order_id=order1.id, worker_id=worker1.id)
    exec2 = Execution(type='type 2', price=1100, service_price=20000, message='working', done_at=datetime(2025, 3, 25, 10, 10), date_recieve=datetime(2025, 9, 12, 10, 10), order_id=order1.id, worker_id=worker1.id)
    exec3 = Execution(type='type 3', price=1500, service_price=10009, message='wait', done_at=datetime(2025, 4, 25, 10, 10), date_recieve=datetime(2022, 6, 1, 10, 10), order_id=order2.id, worker_id=worker2.id)
    exec4 = Execution(type='type 4', price=2000, service_price=500000, message='No', done_at=datetime(2025, 1, 25, 10, 10), date_recieve=datetime(2021, 4, 1, 10, 10), order_id=order2.id, worker_id=worker2.id)

    
    session.add_all([exec1, exec2, exec3, exec4])
    session.commit()

def downgrade() -> None:
    pass
