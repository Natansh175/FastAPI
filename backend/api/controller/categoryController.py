from backend.dto.categoryDTO import CategoryDto, UpdateCategoryDto
from fastapi import APIRouter, Request, Response, HTTPException
from backend.services.categoryServices import CategoryServices
from backend.enum.http_enum import ErrorCode, ErrorDetail
category = APIRouter(
    prefix="/category",
    tags=["category"],
)


@category.post("/insert_category/")
async def create_category(category_insert: CategoryDto, request: Request, response: Response):
    try:
        category_services = CategoryServices()
        if not category_insert:
            response.status_code = ErrorCode.BAD_REQUEST.value
            return HTTPException(detail=ErrorDetail.BadRequest.value, status_code=ErrorCode.BAD_REQUEST.value)

        response_data = category_services.adminInsertCategory(category_insert)
        return response_data

    except Exception as exception:
        print(f"Category Insert Exception: {exception}")
        raise exception


@category.get("/get_categories/")
async def read_categories():
    category_services = CategoryServices()
    return category_services.adminReadCategories()


@category.delete("/delete_category/")
async def delete_category(category_id: int):
    category_services = CategoryServices()
    return category_services.adminDeleteCategory(category_id=category_id)


@category.put("/update_category/", response_model=UpdateCategoryDto)
async def update_category(update_category_id: int, category_update: UpdateCategoryDto):
    category_services = CategoryServices()
    return category_services.adminUpdateCategory(update_category_id=update_category_id, category=category_update)
