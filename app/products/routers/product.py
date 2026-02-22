# from fastapi import APIRouter
# from fastapi.params import Depends
# from fastapi_filter import FilterDepends
# from fastapi_utils.cbv import cbv
#
# from app.products.dependencies import get_product_manager, get_product_or_404
# from app.products.filters import ProductFilter
# from app.products.managers.product_manager import ProductManager
# from app.products.models import Product
# from app.products.schemas import ProductCreate, ProductUpdate
#
# router = APIRouter(
#     prefix="/products",
#     tags=["product"]
# )
#
# @cbv(router)
# class ProductRouter:
#     manager: ProductManager = Depends(get_product_manager)
#
#
#     @router.post("/")
#     async def create(
#             self,
#             request: ProductCreate,
#     ):
#         await self.manager.create_product(request)
#
#
#     @router.get("/")
#     async def list(
#             self,
#             filters: ProductFilter = FilterDepends(ProductFilter),
#     ):
#         products = await self.manager.get_all(filters)
#         return products
#
#
#     @router.get("/{product_id}")
#     async def detail(
#             self,
#             product: Product = Depends(get_product_or_404)
#     ):
#         return product
#
#
#     @router.put("/{product_id}")
#     async def update(
#             self,
#             request: ProductUpdate,
#             product: Product = Depends(get_product_or_404)
#     ):
#         await self.manager.update_product(request, product)
#
#
#     @router.post("/{product_id}")
#     async def delete(
#             self,
#             product: Product = Depends(get_product_or_404)
#     ):
#         await self.manager.delete_product(product)






from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_utils.cbv import cbv

from app.product.dependencies import get_product_manager, get_product_or_404
from app.product.filters import ProductFilter
from app.product.managers.product_manager import ProductManager
from app.product.models import Product
from app.product.schemas import ProductCreate, ProductUpdate, ProductRead, ProductMinRead

router = APIRouter(
    prefix="/product",
    tags=["product"],
)


@cbv(router)
class ProductRouter:
    manager: ProductManager = Depends(get_product_manager)

    @router.get("/", response_model=list[ProductMinRead])
    async def list(
            self,
            filters: ProductFilter = FilterDepends(ProductFilter),

    ):
        return await self.manager.get_all(filters)

    @router.get("/{product_id}", response_model=ProductRead)
    async def get_product(
            self,
            product: Product = Depends(get_product_or_404)
    ):

        return product

    @router.post("/")
    async def create_product(
            self,
            request: ProductCreate,
    ):
        await self.manager.create_product(request)

    @router.put("/{product_id}")
    async def update_product(
            self,
            request: ProductUpdate,
            product: Product = Depends(get_product_manager),
    ):
        await self.manager.update_product(request=request, product=product)

    @router.delete("/{product_id}")
    async def delete_product(
            self,
            product: Product = Depends(get_product_manager),
    ):
        await self.manager.delete_product(product=product)