from fastapi import APIRouter, Depends, UploadFile, File
from fastapi_utils.cbv import cbv
from fastapi.responses import FileResponse

from app.product.dependencies import get_product_or_404, get_product_images_manager, get_product_images_or_404
from app.product.managers.images import ProductImageManager
from app.product.models import Product, ProductImages

router = APIRouter(
    prefix="/{product_id}/images",
    tags=["images"]

)


@cbv(router)
class ImageRouter:
    manager: ProductImageManager = Depends(get_product_images_manager)
    product: Product = Depends(get_product_or_404)

    @router.post("/")
    async def upload(
            self,
            file: UploadFile = File(...)
    ):
        """
        Эндпоинт для загрузки изображения продукта

        Сохраняет файл на диск и создает запись в БД.

        :param file: Загружаемый файл (UploadFile)
        :return: None
        """
        await self.manager.create(product=self.product, file=file)

    @router.get("/{filename}")
    async def get_by_id(
            self,
            image: ProductImages = Depends(get_product_images_or_404),
    ):
        """
        Эндпоинт для получения изображения продукта по имени файла

        Возвращает файл изображения через FileResponse.

        :param image: объект ProductImages, полученный через Depends
        :return: FileResponse с файлом изображения
        """
        return FileResponse(image.file_path)

    @router.delete("/{filename}")
    async def delete(
            self,
            image: ProductImages = Depends(get_product_images_or_404)
    ):
        """
        Эндпоинт для удаления изображения продукта

        Удаляет запись в БД и файл с диска.

        :param image: объект ProductImages, полученный через Depends
        :return: None
        """
        await self.manager.delete(image)