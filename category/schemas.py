from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(max_length=512)
    description: str = Field(max_length=1024)




class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryRead(BaseModel):
    id: int


class CategoryDelete(BaseModel):
    id: int