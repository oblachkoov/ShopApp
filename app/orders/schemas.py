from datetime import datetime
from typing import List

from pydantic import BaseModel, Field
from enum import Enum


class OrdersStatusEnum(str, Enum):
    new = "new"
    paid = "paid"
    completed = "completed"
    cancelled = "cancelled"

class OrderProductsBase(BaseModel):
    product_id: int
    quantity: int = Field(ge=0)
    price: float = Field(ge=0.0)


class OrderProductsCreate(OrderProductsBase):
    status: OrdersStatusEnum = OrdersStatusEnum.new


class OrderProductsUpdate(OrderProductsBase):
    pass


class OrderProductsRead(OrderProductsBase):
    id: int


class OrderBase(BaseModel):
    status: OrdersStatusEnum = OrdersStatusEnum.new
    address: str = Field(max_length=255)
    phone_number: str = Field(max_length=20)
    comment: str = Field(max_length=255)


class OrderCreate(OrderBase):
    products: List[OrderProductsCreate]


class OrderUpdate(OrderBase):
    products: List[OrderProductsUpdate]


class OrderStatusUpdate(BaseModel):
    status: OrdersStatusEnum = OrdersStatusEnum.new


class OrderRead(OrderBase):
    id: int
    created_at: datetime
    products: list[OrderProductsRead]
    user_id: int
    total_sum: float
