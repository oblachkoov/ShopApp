from sqlalchemy import Column, String, Numeric, BigInteger, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.models import IntIdMixin, TimeActionMixin, Base


class Orders(Base, IntIdMixin, TimeActionMixin):
    __tablename__ = 'orders'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    phone_number = Column(String(20), nullable=False)
    address = Column(String(200), nullable=False)
    comment = Column(String(300), nullable=False)
    status = Column(String(20), nullable=False)

    order_products = relationship('OrderProducts', backref='order', lazy='selectin')


class OrdersProducts(Base, IntIdMixin):
    __tablename__ = 'orders_products'

    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    quantity = Column(Numeric(10, 2), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    price = Column(Numeric(20, 2), nullable=False)