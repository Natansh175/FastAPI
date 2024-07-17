from backend.dto.productDTO import ProductDTO, UpdateProductDataDTO
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from backend.services import productServices
from pathlib import Path


product = APIRouter(
    prefix="/product",
    tags=["product"],
)

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}
IMAGE_PATH = "static/userResourses/images"


@product.post("/insert_product/", response_model=ProductDTO)
async def create_product(category_id: int,
                         subcategory_id: int,
                         product_name: str = Form(..., min_length=1),
                         product_description: str = Form(..., min_length=1),
                         product_price: int = Form(..., gt=0),
                         product_quantity: int = Form(..., gt=0),
                         product_image: UploadFile = File(...)
                         ):
    try:
        # To check if uploaded file type is allowed
        if product_image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid image type")

        # Read image data
        product_image_data = await product_image.read()

        product_data = ProductDTO(
            product_name=product_name,
            product_description=product_description,
            product_price=product_price,
            product_quantity=product_quantity,
        )

    except HTTPException as e:
        raise e

    except Exception as ex:
        raise HTTPException(status_code=400, detail=f"Image upload failed: {ex}")

    return productServices.adminInsertProduct(
        category_id,
        subcategory_id,
        product_image.filename,
        product_image_data,
        product_data
    )


@product.get("/get_products/")
async def read_products():
    return productServices.adminReadProducts()


@product.delete("/delete_product/")
async def delete_product(product_id: int):
    return productServices.adminDeleteProduct(product_id)


@product.put("/update_product_data/", response_model=UpdateProductDataDTO)
async def update_product(product_update_id: int, product_update_data: UpdateProductDataDTO):
    return productServices.adminUpdateProductData(product_update_id, product_update_data)


@product.put("/update_product_image/")
async def update_product_image(product_id: int, product_image: UploadFile = File(...)):
    try:
        # To check if uploaded file type is allowed
        if product_image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid image type")

        # To read image data
        product_image_data = await product_image.read()

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"Image upload failed: {e}")

    return productServices.adminUpdateProductImage(product_id,
                                                   product_image.filename,
                                                   product_image_data)
