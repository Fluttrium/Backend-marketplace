from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.dao.base import BaseDAO
from app.exceptions import raise_http_exception
from app.images.router import (
    add_product_image,
    delete_products_file,
    rename_product_image_file,
)

from app.products.categories.dao import ProductCategoryDAO
from app.products.categories.exceptions import ProductCategoryNotFoundException
from app.products.exceptions import (
    ProductAlreadyExistsException,
    ProductNotFoundException,
)
from app.products.models import Product
from app.utils.data import get_new_data
from app.utils.manage import manage_session


class ProductDAO(BaseDAO):
    model = Product

    @classmethod
    @manage_session
    async def add(cls, user, product_data, file, session=None):
        product_data = product_data.model_dump()

        # If user is not admin


        # Validate that category exists
        await cls._validate_category_by_id(product_data["category_id"])

        # Find a product with give name and category
        # (because jeans can have same names, but be for different categories)
        existing_product = await cls.find_one_or_none(
            name=product_data["name"],
            category_id=product_data["category_id"],
        )

        if existing_product:
            raise_http_exception(ProductAlreadyExistsException)

        # Create a product image name as name and category of the product
        product_image_name = (
            product_data["name"].lower().replace(" ", "_").replace("-", "_")
        )

        # Upload the given file to images
        uploaded_image_name = await add_product_image(
            product_image_name, product_data["category_id"], file
        )

        # Add product image to the data
        product_data.update({"product_image": uploaded_image_name})

        # Create the product
        return await cls._create(**product_data)

    @classmethod
    @manage_session
    async def _validate_category_by_id(cls, category_id, session=None):
        product_category = await ProductCategoryDAO.find_by_id(category_id)

        if not product_category:
            raise_http_exception(ProductCategoryNotFoundException)

    @classmethod
    @manage_session
    async def find_by_id(cls, model_id, session=None) -> model:
        query = (
            select(cls.model)
            .options(joinedload(cls.model.category))
            .filter_by(id=model_id)
        )

        result = await session.execute(query)

        product = result.unique().mappings().one_or_none()

        if not product:
            raise_http_exception(ProductNotFoundException)

        return product["Product"]

    @classmethod
    @manage_session
    async def change(cls, product_id, user, data, session=None):
        data = data.model_dump(exclude_unset=True)



        current_product = await cls.validate_by_id(product_id)

        if not current_product:
            return None

        if not data:
            return current_product

        if "category_id" in data:
            if not await ProductCategoryDAO.validate_by_id(
                data["category_id"]
            ):
                raise_http_exception(ProductCategoryNotFoundException)

        new_product_data = get_new_data(current_product, data)

        existing_product = await cls.find_one_or_none(
            name=new_product_data["name"],
            category_id=new_product_data["category_id"],
        )

        if existing_product:
            raise_http_exception(ProductAlreadyExistsException)

        current_product_name = (
            current_product.name.lower().replace(" ", "_").replace("-", "_")
        )
        new_product_name = (
            new_product_data["name"]
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
        )

        new_file = await rename_product_image_file(
            old_name=current_product_name,
            old_category=current_product.category_id,
            new_name=new_product_name,
            new_category=new_product_data["category_id"],
        )

        if new_file:
            data.update({"product_image": new_file})

        return await cls.update_data(product_id, data)

    @classmethod
    @manage_session
    async def change_image(cls, user, file, product_id, session=None):



        product = await cls.find_one_or_none(id=product_id)

        if not product:
            raise_http_exception(ProductNotFoundException)

        current_product_name = (
            product.name.lower().replace(" ", "_").replace("-", "_")
        )

        # Upload the given file to images
        uploaded_image_name = await add_product_image(
            current_product_name, product.category_id, file
        )

        return await cls.update_data(
            product.id, {"product_image": uploaded_image_name}
        )

    @classmethod
    @manage_session
    async def delete(cls, user, product_id, session=None):


        # Get current product
        product = await cls.validate_by_id(product_id)

        if not product:
            raise_http_exception(ProductNotFoundException)

        product_name = product.name.lower().replace(" ", "_").replace("-", "_")

        is_deleted = await delete_products_file(
            product_name, product.category_id
        )

        if not is_deleted:
            return None

        # Delete the product
        await cls.delete_certain_item(product_id)

    @classmethod
    @manage_session
    async def get_product_product_items(cls, product_id, session=None):
        query = (
            select(cls.model)
            .options(joinedload(cls.model.product_items))
            .filter_by(id=product_id)
        )

        result = await session.execute(query)

        product_category = result.unique().mappings().one_or_none()["Product"]

        return product_category
