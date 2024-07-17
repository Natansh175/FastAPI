from fastapi import APIRouter
from backend.api.controller import categoryController, subCategoryController, productController

router = APIRouter()

router.include_router(categoryController.category)
router.include_router(subCategoryController.subCategory)
router.include_router(productController.product)
