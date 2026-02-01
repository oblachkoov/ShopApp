from sqlalchemy import Column, String, Numeric, BigInteger, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.models import IntIdMixin, TimeActionMixin, Base


class Product(Base, IntIdMixin, TimeActionMixin):
    __tablename__ = 'products'
    name = Column(String(512), nullable=False)
    short_description = Column(String(512), nullable=False)
    long_description = Column(String(1024), nullable=False)
    price = Column(Numeric(20, 2), nullable=False)
    category_id = Column(BigInteger, ForeignKey('categories.id', ondelete="RESTRICT"), nullable=False)

    characteristics = relationship(
        'ProductCharacteristic',
        backref='product',
        lazy='selectin',
    )

    reviews = relationship(
        'ProductReview',
        backref='product',
        lazy='selectin',
    )


class ProductCharacteristics(Base, IntIdMixin):
    __tablename__ = 'product_characteristics'
    name = Column(String(512), nullable=False)
    value = Column(String(512), nullable=False)
    product_id = Column(BigInteger, ForeignKey('products.id', ondelete="CASCADE"), nullable=False)



# class ProductImage(Base, IntIdMixin):
#     __tablename__ = 'product_images'



class ProductReview(Base, IntIdMixin):
    __tablename__ = 'product_reviews'
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    product_id = Column(BigInteger, ForeignKey('products.id', ondelete="CASCADE"), nullable=False)
    message = Column(String(2048), nullable=False)
    grade = Column(Integer, nullable=False)