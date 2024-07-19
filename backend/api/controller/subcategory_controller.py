from backend.dto.subcategory_dto import SubCategoryDTO, UpdateSubCategoryDTO
from fastapi import APIRouter
from backend.services import subcategory_services

subCategory = APIRouter(
    prefix="/subcategory",
    tags=["subcategory"],
)


@subCategory.post("/insert_subcategory/", response_model=SubCategoryDTO)
async def create_subcategory(subcategory_insert: SubCategoryDTO, category_id: int):
    return subcategory_services.admin_insert_subcategory(subcategory=subcategory_insert, category_id=category_id)


@subCategory.get("/get_subcategories/")
async def read_subcategories():
    return subcategory_services.admin_read_subcategories()


@subCategory.delete("/delete_subcategory/")
async def delete_subcategory(subcategory_id: int):
    return subcategory_services.admin_delete_subcategory(subcategory_id)


@subCategory.put("/update_subcategory/", response_model=UpdateSubCategoryDTO)
async def update_subcategory(update_subcategory_id: int, subcategory_update: UpdateSubCategoryDTO):
    return subcategory_services.admin_update_subcategory(update_subcategory_id=update_subcategory_id, subcategory=subcategory_update)
