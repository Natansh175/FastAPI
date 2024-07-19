from fastapi import APIRouter

from backend.api.controller import category_controller, subcategory_controller, product_controller

router = APIRouter()

router.include_router(category_controller.category)
router.include_router(subcategory_controller.subCategory)
router.include_router(product_controller.product)
