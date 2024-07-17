from backend.dto.subCategoryDTO import SubCategoryDTO, UpdateSubCategoryDTO
from fastapi import APIRouter
from backend.services import subCategoryServices

subCategory = APIRouter(
    prefix="/subcategory",
    tags=["subcategory"],
)


@subCategory.post("/insert_subcategory/", response_model=SubCategoryDTO)
async def create_subcategory(subcategory_insert: SubCategoryDTO, category_id: int):
    return subCategoryServices.adminInsertSubCategory(subcategory=subcategory_insert, category_id=category_id)


@subCategory.get("/get_subcategories/")
async def read_subcategories():
    return subCategoryServices.adminReadSubCategories()


@subCategory.delete("/delete_subcategory/")
async def delete_subcategory(subcategory_id: int):
    return subCategoryServices.adminDeleteSubCategory(subcategory_id)


@subCategory.put("/update_subcategory/", response_model=UpdateSubCategoryDTO)
async def update_subcategory(update_subcategory_id: int, subcategory_update: UpdateSubCategoryDTO):
    return subCategoryServices.adminUpdateSubCategory(update_subcategory_id=update_subcategory_id, subcategory=subcategory_update)
