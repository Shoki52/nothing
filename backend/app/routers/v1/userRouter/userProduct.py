from typing import List

from app.databases.db import get_db
from app.databases.models.category import Category
from app.databases.models.item import Item
from app.schemas.productSchema.productAllResponseSchema import ProductAllResponseSchema
from app.schemas.productSchema.productCategorySchema import ProductCategorySchema
from app.utils.jwt import JWTUserBearer
from fastapi import APIRouter, Depends
from sqlalchemy import desc, asc
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.schemas.productSchema.productFilterSchema import ProductFilterSchema
from app.schemas.productSchema.productResponseSchema import ProductResponseSchema

UserProduct = APIRouter(tags=["Products of Users"])


@UserProduct.get("/user/products/getAll/", dependencies=[Depends(JWTUserBearer())], response_model=
ProductAllResponseSchema, responses={
    200: {"description": "Get all products"}
}
                 )
async def get_all_products(db: Session = Depends(get_db), skip: int = 0, limit: int = 20):
    q = db.query(Item.id, Item.name, Item.price, Item.photo, Item.description, Item.availability, Item.produced_country,
                 Item.produced_company, Category.name).join(Category, Item.category_id == Category.id).offset(
        skip).limit(limit).all()
    products = []
    for row in q:
        product = {"id": row[0], "name": row[1], "price": row[2], "photo": row[3], "description": row[4],
                   "availability": row[5], "produced_country": row[6], "produced_company": row[7], "category": row[8]}
        products.append(product)
    data = {}
    q2 = db.query(Item.id).count()
    data.update({"products": products, "products_amount": q2})

    return data


@UserProduct.post("/user/products/getAll/filter/", dependencies=[Depends(JWTUserBearer())], response_model=
ProductAllResponseSchema, responses={
    200: {"description": "Get all products with filters(Hint: Sort = 0 - No Sort, 1 - Ascending, 2 - Descending)"},
          400: {"content": {
            "application/json": {
                "example": {"success:": False, "message": "Sort ID is incorrect"}
              }
          }
    }})
async def get_all_products_with_filters(productSchema: ProductFilterSchema, db: Session = Depends(get_db),
                                        skip: int = 0,
                                        limit: int = 20):
    # Без сортировки
    if productSchema.sort == 0:
        if productSchema.availability is None:
            q = db.query(Item.id, Item.name, Item.price, Item.photo, Item.description, Item.availability,
                         Item.produced_country,
                         Item.produced_company, Category.name).join(Category, Item.category_id == Category.id).filter(
                Category.name.like(f"{productSchema.category.lower().capitalize()}%")).filter(
                Item.name.like(f"{productSchema.text.lower().capitalize()}%")).offset(
                skip).limit(limit).all()
            # Подсчет количества
            q2 = db.query(Item.id).join(Category, Item.category_id == Category.id).filter(
                Category.name.like(f"{productSchema.category.lower().capitalize()}%")).filter(
                Item.name.like(f"{productSchema.text.lower().capitalize()}%")).count()
        else:
            q = db.query(Item.id, Item.name, Item.price, Item.photo, Item.description, Item.availability,
                         Item.produced_country,
                         Item.produced_company, Category.name).join(Category, Item.category_id == Category.id).filter(
                Category.name.like(f"{productSchema.category.lower().capitalize()}%")).filter(
                Item.name.like(f"{productSchema.text.lower().capitalize()}%")).filter(Item.availability == productSchema.availability).offset(
                skip).limit(limit).all()
            q2 = db.query(Item.id).join(Category, Item.category_id == Category.id).filter(
                Category.name.like(f"{productSchema.category.lower().capitalize()}%")).filter(
                Item.name.like(f"{productSchema.text.lower().capitalize()}%")).filter(Item.availability == productSchema.availability).count()
    # По возрастанию
    elif productSchema.sort == 1:
        if productSchema.availability is None:
            q = db.query(Item.id, Item.name, Item.price, Item.photo, Item.description, Item.availability,
                         Item.produced_country,
                         Item.produced_company, Category.name).join(Category, Item.category_id == Category.id).filter(
                Category.name.like(f"{productSchema.category.lower().capitalize()}%")).filter(
                Item.name.like(f"{productSchema.text.lower().capitalize()}%")).order_by(
                asc(Item.price)).offset(
                skip).limit(limit).all()
            # Подсчет количества
            q2 = db.query(Item.id).join(Category, Item.category_id == Category.id).filter(
                Category.name.like(f"{productSchema.category.lower().capitalize()}%")).filter(
                Item.name.like(f"{productSchema.text.lower().capitalize()}%")).count()
        else:
            q = db.query(Item.id, Item.name, Item.price, Item.photo, Item.description, Item.availability,
                         Item.produced_country,
                         Item.produced_company, Category.name).join(Category, Item.category_id == Category.id).filter(
                Category.name.like(f"{productSchema.category.lower().capitalize()}%")).filter(
                Item.name.like(f"{productSchema.text.lower().capitalize()}%")).filter(Item.availability == productSchema.availability).order_by(
                asc(Item.price)).offset(
                skip).limit(limit).all()
            q2 = db.query(Item.id).join(Category, Item.category_id == Category.id).filter(
                Category.name.like(f"{productSchema.category.lower().capitalize()}%")).filter(
                Item.name.like(f"{productSchema.text.lower().capitalize()}%")).filter(
                Item.availability == productSchema.availability).count()
    # По убыванию
    elif productSchema.sort == 2:
        if productSchema.availability is None:
            q = db.query(Item.id, Item.name, Item.price, Item.photo, Item.description, Item.availability,
                         Item.produced_country,
                         Item.produced_company, Category.name).join(Category, Item.category_id == Category.id).filter(
                Category.name.like(f"{productSchema.category.lower().capitalize()}%")).filter(
                Item.name.like(f"{productSchema.text.lower().capitalize()}%")).order_by(
                desc(Item.price)).offset(
                skip).limit(limit).all()
            q2 = db.query(Item.id).join(Category, Item.category_id == Category.id).filter(
                Category.name.like(f"{productSchema.category.lower().capitalize()}%")).filter(
                Item.name.like(f"{productSchema.text.lower().capitalize()}%")).count()
        else:
            q = db.query(Item.id, Item.name, Item.price, Item.photo, Item.description, Item.availability,
                         Item.produced_country,
                         Item.produced_company, Category.name).join(Category, Item.category_id == Category.id).filter(
                Category.name.like(f"{productSchema.category.lower().capitalize()}%")).filter(
                Item.name.like(f"{productSchema.text.lower().capitalize()}%")).filter(Item.availability == productSchema.availability).order_by(
                desc(Item.price)).offset(
                skip).limit(limit).all()
            q2 = db.query(Item.id).join(Category, Item.category_id == Category.id).filter(
                Category.name.like(f"{productSchema.category.lower().capitalize()}%")).filter(
                Item.name.like(f"{productSchema.text.lower().capitalize()}%")).filter(
                Item.availability == productSchema.availability).count()
    else:
        return JSONResponse(status_code=400, content={"success:": False, "message": "Sort ID is incorrect"})
    products = []
    for row in q:
        product = {"id": row[0], "name": row[1], "price": row[2], "photo": row[3], "description": row[4],
                   "availability": row[5], "produced_country": row[6], "produced_company": row[7], "category": row[8]}
        products.append(product)
    data = {}
    data.update({"products": products, "products_amount": q2})

    return data


@UserProduct.get("/user/products/get/{product_id}", dependencies=[Depends(JWTUserBearer())], response_model=
ProductResponseSchema, responses={
    200: {"description": "Get product by id"}
})
async def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    q = db.query(Item.id, Item.name, Item.price, Item.photo, Item.description, Item.availability, Item.produced_country,
                 Item.produced_company, Category.name).join(Category, Item.category_id == Category.id).filter(
        Item.id == product_id).first()
    if q is not None:
        product = {"id": q[0], "name": q[1], "price": q[2], "photo": q[3], "description": q[4],
                   "availability": q[5], "produced_country": q[6], "produced_company": q[7], "category": q[8]}
        return product
    else:
        return JSONResponse(status_code=200, content={})


@UserProduct.get('/user/products/getCategory', dependencies=[Depends(JWTUserBearer())],  response_model=List[ProductCategorySchema],
                 responses={
    200: {"description": "Get all categories"}
}
                 )
async def get_all_category(db: Session = Depends(get_db)):
    q = db.query(Category.name, Category.photo).all()
    categories = []
    for row in q:
        data = {"name": row[0], "photo": row[1]}
        categories.append(data)
    return categories

