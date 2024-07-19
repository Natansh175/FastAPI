from datetime import datetime
import os
from pathlib import Path
import uuid

from fastapi import HTTPException

from backend.vo.product_vo import ProductVO
from backend.dao.category_dao import CategoryDAO
from backend.dao.subcategory_dao import SubCategoryDAO
from backend.dao.product_dao import ProductDAO
from backend.dto.product_dto import ProductDTO, UpdateProductDataDTO



IMAGE_PATH = "static/user_resources/images"


# A function to check whether the category or Subcategory is deleted or not
# Prior of performing any activity on subcategory table.
def fk_delete_check(category_id: int, subcategory_id: int):

    category_dao = CategoryDAO()
    subcategory_dao = SubCategoryDAO()

    category_vo_list = category_dao.read_category_immutable(category_id)
    subcategory_vo_list = subcategory_dao.read_subcategory(subcategory_id)

    if category_vo_list is not None and subcategory_vo_list is not None:
        return True
    else:
        pass


def admin_insert_product(category_id: int, subcategory_id: int,
                         image_filename: str,
                         image_data: bytes, product: ProductDTO):
    try:
        category_dao = CategoryDAO()
        subcategory_dao = SubCategoryDAO()
        category_vo_list = category_dao.read_category_immutable(category_id)
        subcategory_vo_list = subcategory_dao.read_subcategory(subcategory_id)

        if category_vo_list is None or subcategory_vo_list is None:
            raise HTTPException(detail="No such Category/Subcategory found with provided ID", status_code=404)

        else:
            unique_id = uuid.uuid4()
            image_unique_filename = f"{unique_id}_{image_filename}"
            image_path = Path(IMAGE_PATH) / image_unique_filename

            # Save the image
            with open(image_path, "wb") as image_file:
                image_file.write(image_data)

            product_vo = ProductVO()
            product_dao = ProductDAO()

            product_vo.product_name = product.product_name
            product_vo.product_description = product.product_description
            product_vo.product_price = product.product_price
            product_vo.product_quantity = product.product_quantity
            product_vo.product_image_name = image_unique_filename
            product_vo.product_image_path = f"/{IMAGE_PATH}/{image_unique_filename}"
            product_vo.is_deleted = False
            product_vo.created_date = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            product_vo.edited_date = ""
            product_vo.product_category_id = category_id
            product_vo.product_subcategory_id = subcategory_id

            product_dao.create_product(product_data=product_vo)
            return product_vo
    except HTTPException as e:
        raise e

    except Exception as ex:
        image_path = Path(IMAGE_PATH) / image_filename
        if image_path.exists():
            os.remove(image_path)
        raise HTTPException(detail=str(ex), status_code=500)


def admin_read_products():
    try:
        category_dao = CategoryDAO()
        subcategory_dao = SubCategoryDAO()
        product_dao = ProductDAO()

        product_data = product_dao.read_products()
        if product_data:

            data_to_show = [
                {
                    "product_id": product.product_id,
                    "product_name": product.product_name,
                    "product_description": product.product_description,
                    "product_price": product.product_price,
                    "product_quantity": product.product_quantity,
                    "product_image": product.product_image_path,
                }
                for product in product_data
                if not category_dao.read_category_immutable(
                    product.product_category_id) is None
                and not subcategory_dao.read_subcategory(
                    product.product_subcategory_id) is None
            ]

            if data_to_show:
                return data_to_show
            else:
                raise HTTPException(detail="No Products to show", status_code=404)
        else:
            raise HTTPException(detail="No Products to show", status_code=404)

    except HTTPException as ex:
        raise ex

    except Exception as ex:
        raise HTTPException(detail=str(ex), status_code=500)


def admin_delete_product(product_id: int):
    try:
        product_dao = ProductDAO()
        product_vo_list = product_dao.edit_product(product_id)

        if product_vo_list is not None and product_vo_list.is_deleted == 0:

            delete_check = fk_delete_check(
                product_vo_list.product_category_id, product_vo_list.product_subcategory_id)
            if delete_check is None:
                raise HTTPException(status_code=500, detail="Cannot find category/subcategory with this ID")

            else:

                product_vo_list.is_deleted = True
                product_dao.update_product(product_vo_list)

                return {"Message": "Product deleted successfully"}

        elif product_vo_list is None or product_vo_list.is_deleted == 1:
            return HTTPException(detail="Cannot find Product with this ID", status_code=500)

    except HTTPException as ex:
        raise ex

    except Exception as ex:
        raise HTTPException(detail=str(ex), status_code=500)


def admin_update_product_data(product_update_id: int, product_update_data:
                              UpdateProductDataDTO):
    try:
        product_dao = ProductDAO()
        product_vo_list = product_dao.edit_product(product_update_id)

        if product_vo_list is not None and product_vo_list.is_deleted == 0:
            delete_value = fk_delete_check(
                product_vo_list.product_category_id, product_vo_list.product_subcategory_id)

            if delete_value is None:
                raise HTTPException(status_code=500, detail="Cannot find Category/subcategory with this ID")

            else:
                product_data = product_update_data.model_dump(exclude_unset=True)
                for key, value in product_data.items():
                    setattr(product_vo_list, key, value)

                product_vo_list.edited_date = datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M')

                product_dao.update_product(product_vo_list=product_vo_list)
                return product_vo_list

        elif product_vo_list is None or product_vo_list.is_deleted == 1:
            raise HTTPException(status_code=404, detail="Cannot find Product with this ID")

    except HTTPException as ex:
        raise ex

    except Exception as ex:
        raise HTTPException(detail=str(ex), status_code=500)


def admin_update_product_image(update_image_id: int, update_image_name: str,
                               product_image_data: bytes):
    try:
        product_dao = ProductDAO()

        product_vo_list = product_dao.edit_product(update_image_id)

        if product_vo_list is not None and product_vo_list.is_deleted == 0:

            delete_check = fk_delete_check(
                product_vo_list.product_category_id, product_vo_list.product_subcategory_id)
            if delete_check is None:
                os.remove(os.path.join(IMAGE_PATH, update_image_name))
                raise HTTPException(status_code=500, detail="Cannot find Category/subcategory with this ID")
            else:
                previous_product_image = product_vo_list.product_image_name
                os.remove(os.path.join(IMAGE_PATH, previous_product_image))


                unique_id = uuid.uuid4()
                image_unique_filename = f"{unique_id}_{update_image_name}"
                image_path = Path(IMAGE_PATH) / image_unique_filename

                # Save the image
                with open(image_path, "wb") as image_file:
                    image_file.write(product_image_data)

                product_vo_list.product_image_name = image_unique_filename
                product_vo_list.edited_date = datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M')
                product_vo_list.product_image_path = f"/{IMAGE_PATH}/{image_unique_filename}"
                product_dao.update_product(product_vo_list=product_vo_list)
                return {"Message": "Product Image Updated successfully"}

        elif product_vo_list is None or product_vo_list.is_deleted == 1:
            raise HTTPException(status_code=404, detail="Cannot find Product with this ID")

    except HTTPException as ex:
        raise ex

    except Exception as ex:
        raise HTTPException(detail=str(ex), status_code=500)
