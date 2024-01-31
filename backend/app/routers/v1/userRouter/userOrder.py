from datetime import datetime
from typing import List
import pytz as pytz
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy import insert, func, select, desc
from sqlalchemy.orm import Session
from app.databases.db import get_db
from app.schemas.orderSchema.orderAmountSchema import OrderAmountSchema
from app.schemas.orderSchema.orderCreateSchema import OrderCreateSchema
from app.schemas.orderSchema.orderResponseSchema import OrderResponseSchema
from app.utils.jwt import JWTUserBearer
from app.databases.models.order import Order
from app.utils.jwt import decodeToken
from app.databases.models.user import User
from app.databases.models.order_item import orders_items
from app.databases.models.item import Item
from app.databases.models.category import Category
from app.schemas.orderSchema.orderResponseByIdSchema import OrderResponseByIdSchema

UserOrder = APIRouter(tags=["Orders of Users"])


@UserOrder.post("/user/orders/create", dependencies=[Depends(JWTUserBearer())], responses={
    400: {"content": {
            "application/json": {
                "example": {"success:": False, "message": "Product ID is incorrect"}
              }
          }
    },
    200: {"description": "Create Order for User", "content":
        {"application/json": {
            "example": {"success": True}
        }
    }
}
})
async def create_order(orderCreate: OrderCreateSchema, request: Request, db: Session = Depends(get_db)):
    try:
        products = orderCreate.dict()["products"]
        # Проверка item_id в БД
        for i in products:
            item_id = i["id"]
            q = db.query(Item.id).filter(Item.id == item_id).first()
            if q is None:
                return JSONResponse(status_code=400, content={"success": False, "message": "Product ID is incorrect"})
        # Authorization - хедер, где хранится токен
        authorization = request.headers.get("Authorization")
        # Убираю из начала Bearer
        access_token = authorization.replace("Bearer ", "")
        # Достаю данные из payload
        payload = await decodeToken(access_token)
        user_phone_int = payload["phone_int"]
        # Время в Казахстане
        kz_timezone = pytz.timezone('Asia/Almaty')
        # Получение времени создания заказа по UTC
        current_time = datetime.now(kz_timezone).strftime("%Y-%m-%d %H:%M:%S")
        # Запрос, чтоб получить id от User
        q = db.query(User.id).filter(User.phone_number == user_phone_int).first()
        user_id = q[0]
        # Создать запись в таблице Order
        order = Order(user_id=user_id, address=orderCreate.delivery_address, status=orderCreate.delivery_status,
                      date=current_time)
        db.add(order)
        db.commit()
        products = orderCreate.dict()["products"]
        # Достаю продукты из списка
        for i in products:
            item_id = i["id"]
            amount = i["amount"]
            # Создать запись в таблице Order_Item
            values = {"order_id": order.id, "item_id": item_id, "amount": amount}
            stmt = orders_items.insert().values(values)
            db.execute(stmt)
            db.commit()
        return JSONResponse(status_code=200, content={"success": True})
    except:
        return JSONResponse(status_code=400, content={"success": False})


@UserOrder.get("/user/orders/getAll", dependencies=[Depends(JWTUserBearer(

))], response_model=List[OrderResponseSchema])
async def get_all_orders(request: Request, db: Session = Depends(get_db),
                         skip: int = 0, limit: int = 20):
    # Authorization - хедер, где хранится токен
    authorization = request.headers.get("Authorization")
    # Убираю из начала Bearer
    access_token = authorization.replace("Bearer ", "")
    # Достаю данные из payload
    payload = await decodeToken(access_token)
    user_phone_int = payload["phone_int"]
    # Запрос, чтоб получить id от User
    q = db.query(User.id).filter(User.phone_number == user_phone_int).first()
    user_id = q[0]
    # Получаю данные о Order по user_id
    q = db.query(Order.id, Order.status, Order.address).filter(
        Order.user_id == user_id).order_by(
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


@UserOrder.get("/user/orders/get/{order_id}", dependencies=[Depends(JWTUserBearer())], response_model=OrderResponseByIdSchema)
async def get_order_by_id(request: Request, order_id: int, db: Session = Depends(get_db)):
    # Authorization - хедер, где хранится токен
    authorization = request.headers.get("Authorization")
    # Убираю из начала Bearer
    access_token = authorization.replace("Bearer ", "")
    # Достаю данные из payload
    payload = await decodeToken(access_token)
    user_phone_int = payload["phone_int"]
    # Запрос, чтоб получить id от User
    q = db.query(User.id).filter(User.phone_number == user_phone_int).first()
    user_id = q[0]
    # Получаю данные о Order по user_id
    q = db.query(Order.id, Order.status, Order.address).filter(
        Order.id == order_id, Order.user_id == user_id).first()
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
            stmt2 = select(Item.price, Item.name, Item.photo, Item.description, Item.availability, Item.produced_country, Item.produced_company, Category.name).join(Category, Item.category_id == Category.id).where(Item.id == item_id)
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
                product = {"id": item_id, "name": item_name, "price": price, "photo": item_photo, "description": item_description,
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


@UserOrder.get("/user/orders/getAmount", dependencies=[Depends(JWTUserBearer())], response_model=OrderAmountSchema,
               responses={
    200: {"description": "Get amount of Orders"}})
async def get_amount_of_orders(request: Request, db: Session = Depends(get_db)):
    # Authorization - хедер, где хранится токен
    authorization = request.headers.get("Authorization")
    # Убираю из начала Bearer
    access_token = authorization.replace("Bearer ", "")
    # Достаю данные из payload
    payload = await decodeToken(access_token)
    user_phone_int = payload["phone_int"]
    # Запрос, чтоб получить id от User
    q = db.query(User.id).filter(User.phone_number == user_phone_int).first()
    user_id = q[0]
    # Получаю данные о Order по user_id
    q = db.query(Order.id).filter(Order.user_id == user_id).count()
    data = {"amount": q}
    return JSONResponse(status_code=200, content=data)
