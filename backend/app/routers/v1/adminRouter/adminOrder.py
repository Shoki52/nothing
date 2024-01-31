from typing import List
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends

from app.schemas.orderSchema.orderAmountSchema import OrderAmountSchema
from app.schemas.orderSchema.orderUpdateSchema import OrderUpdateSchema
from app.utils.jwt import JWTUserBearer
from app.databases.db import get_db
from sqlalchemy import select, update, delete, desc
from sqlalchemy.orm import Session
from app.databases.models.order import Order
from app.databases.models.order_item import orders_items
from app.databases.models.item import Item
from app.schemas.orderSchema.orderResponseSchema import OrderResponseSchema
from app.schemas.orderSchema.orderResponseByIdSchema import OrderResponseByIdSchema
from app.databases.models.category import Category

AdminOrder = APIRouter(tags=["Orders of Admins"])


@AdminOrder.get("/admin/orders/getAll/", dependencies=[Depends(JWTUserBearer(admin=True))],
                response_model=List[OrderResponseSchema])
async def get_all_orders_for_admin(db: Session = Depends(get_db), skip: int = 0, limit: int = 20):
    # Получаю данные о Order по user_id
    q = db.query(Order.id, Order.status, Order.address).order_by(
                desc(Order.date)).offset(skip).limit(limit).all()
    data = []
    for row in q:
        order_id = row[0]
        delivery_status = row[1]
        delivery_address = row[2]
        order = {"order_id": order_id, "delivery_status": delivery_status, "delivery_address": delivery_address}
        # id товаров + amount товара
        stmt = select(orders_items.c.item_id, orders_items.c.amount).where(orders_items.c.order_id == order_id)
        item_ids_with_amount = db.execute(stmt).fetchall()
        order_price = 0
        # Подсчет цены
        for i in item_ids_with_amount:
            item_id = i[0]
            amount = i[1]
            # Цена каждого товара в таблице Item
            stmt2 = select(Item.price).where(Item.id == item_id)
            result = db.execute(stmt2).fetchall()
            price = result[0][0]
            # Подсчет общей цены, относительно количества
            order_price = order_price + price * amount
        # Добавляем в JSON
        order.update({"order_price": order_price})
        data.append(order)
    return data


@AdminOrder.get("/admin/orders/get/{order_id}", dependencies=[Depends(JWTUserBearer(admin=True))],
                response_model=OrderResponseByIdSchema)
async def get_order_by_id_for_admin(order_id: int, db: Session = Depends(get_db)):
    # Получаю данные о Order по user_id
    q = db.query(Order.id, Order.status, Order.address).filter(
        Order.id == order_id).first()
    if q is None:
        return JSONResponse(status_code=200, content={})
    else:
        order_id = q[0]
        delivery_status = q[1]
        delivery_address = q[2]
        order = {"order_id": order_id, "delivery_status": delivery_status, "delivery_address": delivery_address}
        # id товаров + amount товара
        stmt = select(orders_items.c.item_id, orders_items.c.amount).where(orders_items.c.order_id == order_id)
        item_ids_with_amount = db.execute(stmt).fetchall()
        order_price = 0
        products_amount = 0
        products = []
        # Получение ID и количества
        for i in item_ids_with_amount:
            item_id = i[0]
            amount = i[1]
            # Информация каждого товара в таблице Item
            stmt2 = select(Item.price, Item.name, Item.photo, Item.description, Item.availability,
                           Item.produced_country, Item.produced_company, Category.name).join(Category,
                                                                                             Item.category_id == Category.id).where(
                Item.id == item_id)
            result = db.execute(stmt2).fetchall()
            # Row все равно один, поскольку не может быть несколько товаров с одинаковым id, поэтому можно все в цикле оставить
            for row in result:
                price = row[0]
                item_name = row[1]
                item_photo = row[2]
                item_description = row[3]
                item_availability = row[4]
                item_produced_country = row[5]
                item_produced_company = row[6]
                item_category = row[7]
                product = {"id": item_id, "name": item_name, "price": price, "photo": item_photo,
                           "description": item_description,
                           "availability": item_availability, "produced_country": item_produced_country,
                           "produced_company": item_produced_company, "amount": amount, "category": item_category}
                # Подсчет общей цены, относительно количества
                order_price = order_price + price * amount
                # Подсчет общего количества продуктов
                products_amount = products_amount + amount
                products.append(product)
        order.update({"order_price": order_price, "products_amount": products_amount})
        order.update({"products": products})
        return order


@AdminOrder.put("/admin/orders/update/{order_id}", dependencies=[Depends(JWTUserBearer(admin=True))], responses={
    200: {"description": "Update order by id",
          "content": {
              "application/json": {
                  "example": {"success": True, "message": "Order was updated"}
              }
          }
          },
    400: {"content": {
        "application/json": {
            "example": {"success": False, "message": "Order ID is incorrect"}
        }
    }
    }

})
async def update_order_status(order_id: int, orderUpdate: OrderUpdateSchema, db: Session = Depends(get_db)):
    q = db.query(Order).filter(Order.id == order_id).first()
    # Если есть такой товар
    if q:
        data = {"status": orderUpdate.delivery_status}
        stmt = (update(Order).where(Order.id == order_id).values(**data))
        db.execute(stmt)
        db.commit()
        return JSONResponse(status_code=200, content={"success": True, "message": "Order was updated"})
    else:
        return JSONResponse(status_code=400, content={"success": False, "message": "Order ID is incorrect"})


@AdminOrder.delete("/admin/orders/delete/{order_id}", dependencies=[Depends(JWTUserBearer(admin=True))], responses={
    200: {"description": "Delete order by id",
          "content": {
              "application/json": {
                  "example": {"success": True, "message": "Order was deleted"}
              }
          }
          },
    400: {"content": {
        "application/json": {
            "example": {"success": False, "message": "Order ID is incorrect"}
        }
    }
    }

})
async def delete_order_by_id(order_id: int, db: Session = Depends(get_db)):
    q = db.query(Order).filter(Order.id == order_id).first()
    # Если есть такой товар
    if q:
        # Удалить из orders_items
        stmt = (delete(orders_items).where(orders_items.c.order_id == order_id))
        db.execute(stmt)
        db.commit()
        # Удалить из order
        stmt = (delete(Order).where(Order.id == order_id))
        db.execute(stmt)
        db.commit()
        return JSONResponse(status_code=200, content={"success": True, "message": "Order was deleted"})

    else:
        return JSONResponse(status_code=400, content={"success": False, "message": "Order ID is incorrect"})


@AdminOrder.get("/admin/orders/getAmount", dependencies=[Depends(JWTUserBearer(admin=True))],
                response_model=OrderAmountSchema, responses={
    200: {"description": "Get amount of Orders"}})
async def get_amount_of_orders_for_admin(db: Session = Depends(get_db)):
    q = db.query(Order.id).filter().count()
    data = {"amount": q}
    return JSONResponse(status_code=200, content=data)
