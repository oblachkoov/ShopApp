from pydantic import BaseModel, Field, field_validator

from app.core.schemas import TimeActionSchema


class ProductCharacteristicsBase(BaseModel):
    product_name: str = Field(max_length=512)
    value: str = Field(max_length=512)


class ProductCharacteristicsCreate(ProductCharacteristicsBase):
    pass


class ProductCharacteristicsUpdate(ProductCharacteristicsBase):
    pass


class ProductCharacteristicsRead(ProductCharacteristicsBase):
    pass

class ProductReviewBase(BaseModel):
    message: str = Field(max_length=2048)
    grade: int = Field(ge=0, le=5)


class ProductReviewCreate(ProductReviewBase):
    pass


class ProductReviewUpdate(ProductReviewBase):
    pass


class ProductReviewRead(ProductReviewBase, TimeActionSchema):
    id: int
    user_id: int



class ProductBase(BaseModel):
    product_name: str = Field(min_length=512)
    product_short_description: str = Field(max_length=512)
    product_price: float = Field(max_digits=20, decimal_places=2)
    product_category_id: int


class ProductCreate(ProductBase):
    category_id: int = Field(ge=1)
    product_long_description: str


class ProductUpdate(ProductBase):
    product_long_description: str


class ProductMinRead(ProductBase):
    id: int
    rating: float = 0
    reviews_count: int = 0
    #image



class ProductRead(ProductMinRead, TimeActionSchema):
    category_id: int = Field(ge=1)
    product_long_description: str

    reviews: list[ProductReviewRead]
    characteristics: list[ProductCharacteristicsRead]



