from fastapi import APIRouter

from backend.api.controller import (category_controller,
                                    subcategory_controller,
                                    product_controller,
                                    authentication_controller)


# APIRouter object to include other APIRouter classes across the project
# Ultimately included in the app on main file
router = APIRouter()

# Sub-App routers
router.include_router(authentication_controller.authentication)
router.include_router(category_controller.category)
router.include_router(subcategory_controller.subCategory)
router.include_router(product_controller.product)
