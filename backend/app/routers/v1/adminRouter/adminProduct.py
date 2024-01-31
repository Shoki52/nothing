import time

from fastapi import APIRouter, Depends, UploadFile, HTTPException, File
from fastapi.responses import JSONResponse

from app.databases.s3 import s3_upload_image, s3_uploadobj, s3_create_download_link, s3_deleteobj
from app.routers.v1.userRouter.userProduct import get_all_category, get_all_products_with_filters, get_all_products, \
    get_product_by_id
from sqlalchemy import delete, update
from sqlalchemy.orm import Session
from app.databases.db import get_db
from app.schemas.productSchema.productAllResponseSchema import ProductAllResponseSchema
from app.utils.jwt import JWTUserBearer
from app.databases.models.item import Item
from app.databases.models.category import Category
from app.databases.models.order_item import orders_items
from app.schemas.productSchema.productCreateSchema import ProductCreateSchema
from app.schemas.productSchema.productResponseSchema import ProductResponseSchema
from app.schemas.productSchema.productFilterSchema import ProductFilterSchema
from app.schemas.productSchema.productUpdateSchema import ProductUpdateSchema

AdminProduct = APIRouter(tags=["Products of Admins"])


@AdminProduct.post("/admin/products/create", dependencies=[Depends(JWTUserBearer(admin=True))], responses={
    200: {"description": "Create product",
          "content": {
              "application/json": {
                  "example": {"success:": True, "message": "Product was added"}
              }
          }
          },
    400: {
        "content": {
            "application/json": {
                "example": {"success": False, "message": "Category name is incorrect"}
            }
        }
    }
})
async def create_product(createOrder: ProductCreateSchema,
                         db: Session = Depends(get_db)):
    q = db.query(Category.id).filter(
        Category.name == createOrder.category).first()
    if q:
        category = q[0]
        link = ""
        # Добавляю продукт
        item = Item(category_id=category, name=createOrder.name, price=createOrder.price, photo=link
                    , description=createOrder.description,
                    availability=createOrder.availability,
                    produced_country=createOrder.produced_country, produced_company=createOrder.produced_company)
        db.add(item)
        db.commit()
        return JSONResponse(status_code=200,
                            content={"success": True, "message": "Product was added", "product_id": item.id})
    else:
        return JSONResponse(status_code=400, content={"success": False, "message": "Category name is incorrect"})


@AdminProduct.get("/admin/products/getAll/", dependencies=[Depends(JWTUserBearer(admin=True))], response_model=
ProductAllResponseSchema, responses={
    200: {"description": "Get all products"}
})
async def get_all_products_for_admin(db: Session = Depends(get_db), skip: int = 0, limit: int = 20):
    data = await get_all_products(db, skip, limit)
    return data


@AdminProduct.post("/admin/products/getAll/filter/", dependencies=[Depends(JWTUserBearer(admin=True))], response_model=
ProductAllResponseSchema, responses={
    200: {"description": "Get all products with filters(Hint: Sort = 0 - No Sort, 1 - Ascending, 2 - Descending)"},
    400: {"content": {
        "application/json": {
            "example": {"success:": False, "message": "Sort ID is incorrect"}
        }
    }
    }})
async def get_all_products_with_filters_for_admin(productSchema: ProductFilterSchema, db: Session = Depends(get_db),
                                                  skip: int = 0, limit: int = 20):
    data = await get_all_products_with_filters(productSchema, db, skip, limit)
    return data


@AdminProduct.get("/admin/products/get/{product_id}", dependencies=[Depends(JWTUserBearer(admin=True))], response_model=
ProductResponseSchema, responses={
    200: {"description": "Get product by id"}
})
async def get_product_by_id_for_admin(product_id: int, db: Session = Depends(get_db)):
    product = await get_product_by_id(product_id, db)
    return product


@AdminProduct.put("/admin/products/update/{product_id}", dependencies=[Depends(JWTUserBearer(admin=True))], responses={
    200: {"description": "Update product",
          "content": {
              "application/json": {
                  "example": {"success:": True, "message": "Product was updated"}
              }
          }
          },
    400: {"content": {
        "application/json": {
            "example": {"success": False, "message": "Product ID is incorrect"}
        }
    }
    },
    401: {"content": {
        "application/json": {
            "example": {"success": False, "message": "Category is incorrect"}
        }
    }
    }

})
async def update_product_by_id_for_admin(productUpdate: ProductUpdateSchema, product_id: int,
                                         db: Session = Depends(get_db)):
    q = db.query(Item).filter(Item.id == product_id).first()
    # Если есть такой товар
    if q:
        data = dict(productUpdate)
        # Преобразовать в словарь для изменяемых данных
        filtered_data = {key: value for key, value in data.items() if (value is not None and key != "category")}
        # Если хотят изменить категорию
        if productUpdate.category is not None:
            # Получить Category ID
            q = db.query(Category.id).filter(
                Category.name == productUpdate.category).first()
            # Добавить Category ID
            if q:
                category_id = q[0]
                filtered_data.update({"category_id": category_id})
            else:
                return JSONResponse(status_code=401, content={"success": False, "message": "Category is incorrect"})
        stmt = (update(Item).where(Item.id == product_id).values(**filtered_data))
        db.execute(stmt)
        db.commit()
        return JSONResponse(status_code=200, content={"success": True, "message": "Product was updated"})

    else:
        return JSONResponse(status_code=400, content={"success": False, "message": "Product ID is incorrect"})


@AdminProduct.delete("/admin/products/delete/{product_id}", dependencies=[Depends(JWTUserBearer(admin=True))],
                     responses={
                         200: {"description": "Delete product by id",
                               "content": {
                                   "application/json": {
                                       "example": {"success": True, "message": "Product was deleted"}
                                   }
                               }
                               },
                         400: {"content": {
                             "application/json": {
                                 "example": {"success": False, "message": "Product ID is incorrect"}
                             }
                         }
                         },
                         500: {"content": {
                             "application/json": {
                                 "example": {"detail": "Something went wrong"}
                             }
                         }
                         }

                     })
async def delete_product_by_id_for_admin(product_id: int, db: Session = Depends(get_db)):
    q = db.query(Item.photo).filter(Item.id == product_id).first()
    link = q[0]
    # Если есть такой товар
    if q:
        # Удаление изображения из S3, если оно есть
        if link != "":
            file_name = link.replace("https://sara.hb.kz-ast.vkcs.cloud/", "")
            if await s3_deleteobj(file_name):
                pass
                # Изменяю запись в БД
            else:
                raise HTTPException(status_code=500, detail='Something went wrong')

        stmt = (delete(orders_items).where(orders_items.c.item_id == product_id))
        db.execute(stmt)
        db.commit()
        stmt = (delete(Item).where(Item.id == product_id))
        db.execute(stmt)
        db.commit()
        return JSONResponse(status_code=200, content={"success": True, "message": "Product was deleted"})
    else:
        return JSONResponse(status_code=400, content={"success": False, "message": "Product ID is incorrect"})


@AdminProduct.get("/admin/products/getCategory", dependencies=[Depends(JWTUserBearer(admin=True))], responses={
    200: {"description": "Get all categories",
          "content":
              {"application/json": {
                  "example": ["Категория1", "Категория2"]
              }
              }}
})
async def get_all_category_for_admin(db: Session = Depends(get_db)):
    q = db.query(Category.name).all()
    categories = []
    for row in q:
        categories.append(row[0])
    return categories


@AdminProduct.post("/admin/products/updatePhoto/{product_id}", dependencies=[Depends(JWTUserBearer(admin=True))],
                   responses={
                       200: {"description": "Update product photo by id",
                             "content": {
                                 "application/json": {
                                     "example": {"success": True, "message": "Photo was updated"}
                                 }
                             }
                             },
                       400: {"content": {
                           "application/json": {
                               "example": {"success": False, "message": "Product ID is incorrect"}
                           }
                       }
                       },
                       500: {"content": {
                           "application/json": {
                               "example": {"detail": "Something went wrong"}
                           }
                       }
                       }
                   })
async def update_photo(product_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Поиск такого товара
    q = db.query(Item.photo).filter(
        Item.id == product_id).first()
    if q:
        link = q[0]
        try:
            # открываю в бинарном виде
            file.file.seek(0)
            timestamp = time.time()
            # Новое название файла
            obj_name = f'{timestamp}.jpg'
            # Загружаю новое изображение
            await s3_uploadobj(file.file, obj_name)
            # Создание новой ссылки
            new_link = await s3_create_download_link(obj_name)
            data = {"photo": new_link}
            # Если было старое
            if link != "":
                file_name = link.replace("https://sara.hb.kz-ast.vkcs.cloud/", "")
                # Попытка удалить предыдущий файл
                if await s3_deleteobj(file_name):
                    # Изменяю запись в БД
                    stmt = (update(Item).where(Item.id == product_id).values(**data))
                    db.execute(stmt)
                    db.commit()
                    return JSONResponse(status_code=200, content={"success": True, "message": "Photo was updated"})
                else:
                    raise HTTPException(status_code=500, detail='Something went wrong')
            else:
                # Изменяю запись в БД
                stmt = (update(Item).where(Item.id == product_id).values(**data))
                db.execute(stmt)
                db.commit()
                return JSONResponse(status_code=200, content={"success": True, "message": "Photo was updated"})
        except Exception:
            raise HTTPException(status_code=500, detail='Something went wrong')
        finally:
            file.file.close()
    else:
        return JSONResponse(status_code=400, content={"success": False, "message": "Product ID is incorrect"})
