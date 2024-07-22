from enum import Enum


class HttpStatusCodeEnum(int, Enum):
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    TEMPORARY_REDIRECT = 303
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    UNPROCESSABLE_ENTITY = 422
    INTERNAL_SERVER_ERROR = 500


class ResponseMessageEnum(str, Enum):
    # For Category CRUD
    CategoryCreated = "Category Created Successfully."
    CategoryDeleted = "Category Deleted Successfully."
    CategoryUpdated = "Category Updated Successfully."
    CategoryNotFound = "Cannot find Category with provided ID."
    NoCategoryFound = "No Categories to show!"
    CategoryUnprocessableEntity = "Make sure you entered a Name/Description and category count is greater than zero."

    # For SubCategory CRUD
    SubCategoryCreated = "SubCategory Created Successfully."
    SubCategoryDeleted = "SubCategory Deleted Successfully."
    SubCategoryUpdated = "SubCategory Updated Successfully."
    SubCategoryCategoryNotFound = "Cannot find Category with provided ID."
    SubCategoryNotFound = "Cannot find SubCategory with provided ID."
    NoSubCategoryFound = "No SubCategories to show!"
    SubCategoryUnprocessableEntity = "Make sure you entered a Name/Description and SubCategory count is greater than zero."

    # For Product CRUD
    ProductCreated = "Product Created Successfully."
    ProductDeleted = "Product Deleted Successfully."
    ProductUpdated = "Product Updated Successfully."
    ProductImageUpdate = "Product Image Updated Successfully."
    ProductNotFound = "Cannot find Product with provided ID."
    NoProductFound = "No Products to show!"
    ProductUnprocessableEntity = "Make sure you entered a Name/Description and Product quantity/price is greater than zero."

    # Server Error
    InternalServerError = "Internal Server Error."

    # Client Error
    BadRequest = "Oops! Bad Request."
    OK = "Request Processed Successfully."
