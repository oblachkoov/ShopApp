from sqlalchemy import Column, String, Numeric, ForeignKey, Integer, UniqueConstraint, select, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.core.models import IntIdMixin, TimeActionMixin, Base


class Orders(Base, IntIdMixin, TimeActionMixin):
    __tablename__ = 'orders'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    phone_number = Column(String(20), nullable=False)
    address = Column(String(200), nullable=False)
    comment = Column(String(300), nullable=False)
    status = Column(String(20), nullable=False)

    products = relationship('OrderProducts', backref='order', lazy='selectin')

    @hybrid_property
    def total_sum(self):
        return sum(product.quantity * product.price for product in self.products)

    @total_sum.expression
    def total_sum(cls):
        return(
            select(
                func.sum(OrdersProducts.quantity * OrdersProducts.price)
                .where(OrdersProducts.order_id == cls.id)
                .scalar_subquery()
            )
        )



class OrdersProducts(Base, IntIdMixin):
    __tablename__ = 'orders_products'

    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    quantity = Column(Numeric(10, 2), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    price = Column(Numeric(20, 2), nullable=False)
    __table_args__ = (
        UniqueConstraint('order_id', 'product_id', name='orders_products_unique_id'),
    )

