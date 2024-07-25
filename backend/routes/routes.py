from fastapi import APIRouter

from backend.api.controller import (category_controller,
                                    subcategory_controller,
                                    product_controller, register_controller,
                                    login_controller)


# APIRouter object to include other APIRouter classes across the project
# Ultimately included in the app
router = APIRouter()

# Includes sub-app routers
router.include_router(register_controller.register)
router.include_router(login_controller.login)
router.include_router(category_controller.category)
router.include_router(subcategory_controller.subCategory)
router.include_router(product_controller.product)
