from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from app.routers.v1.userRouter.userAuth import UserAuth
from app.routers.v1.userRouter.userProduct import UserProduct
from app.routers.v1.userRouter.userOrder import UserOrder
from app.routers.v1.adminRouter.adminAuth import AdminAuth
from app.routers.v1.adminRouter.adminProduct import AdminProduct
from app.routers.v1.adminRouter.adminOrder import AdminOrder

# Само приложение
app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc", openapi_url="/api/openapi.json")

# Подключение CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роутеры пользователей
app.include_router(UserAuth, prefix="/api")
app.include_router(UserProduct, prefix="/api")
app.include_router(UserOrder, prefix="/api")
# Роутеры админов
app.include_router(AdminAuth, prefix="/api")
app.include_router(AdminProduct, prefix="/api")
app.include_router(AdminOrder, prefix="/api")

from sqlalchemy.orm import Session
from app.databases.db import get_db
from app.databases.models.category import Category
from app.databases.models.item import Item
from fastapi import Depends
from app.databases.s3 import s3_create_download_link


# На время мок-генератор
@app.get("/api/mock_generator")
async def mock_generate(password: str = Header(default=None), db: Session = Depends(get_db)):
    if password == "da_da_super_parol":
        try:
            link = await s3_create_download_link('lays.jpg')
            item = Item(category_id=5, name="Чипсы", price=300, photo=link, description="Много воздуха, мало чипсов",
                        availability=True,
                        produced_country="kz", produced_company="Lays")
            db.add(item)
            db.commit()
            link = await s3_create_download_link('kirieshki.jpg')
            item = Item(category_id=5, name="Сухарики", price=150, photo=link, description="Скажи привет, проблемам с зубами",
                         availability=True,
                         produced_country="kz", produced_company="Кириешки")
            db.add(item)
            db.commit()
            link = await s3_create_download_link('shymkent.jpg')
            item = Item(category_id=2, name="Пиво", price=440, photo=link, description="Тебе точно завтра будет плохо",
                         availability=True,
                         produced_country="kz", produced_company="Шымкентское")
            db.add(item)
            db.commit()
            link = await s3_create_download_link('vino.jpg')
            item = Item(category_id=2, name="Вино", price=3000, photo=link, description="Для настоящих аристократов",
                         availability=True,
                         produced_country="fr", produced_company="")
            db.add(item)
            db.commit()
            link = await s3_create_download_link('pomidory.jpg')
            item = Item(category_id=1, name="Помидоры", price=500, photo=link, description="Розовые",
                        availability=True,
                        produced_country="kz", produced_company="")
            db.add(item)
            db.commit()
            link = await s3_create_download_link('banana.jpg')
            item = Item(category_id=1, name="Бананы", price=900, photo=link, description="Нормальный человек не покупает поштучно",
                        availability=True,
                        produced_country="ecu", produced_company="Bananchelo")
            db.add(item)
            db.commit()
            link = await s3_create_download_link('richmond_vishnya.jpg')
            item = Item(category_id=3, name="Richmond Вишня", price=1200, photo=link,
                        description="Твои легкие не скажут спасибо",
                        availability=True,
                        produced_country="us", produced_company="Richmond")
            db.add(item)
            db.commit()
            db.commit()
            link = await s3_create_download_link('winston_sinie.jpg')
            item = Item(category_id=3, name="Winston Синие", price=1070, photo=link,
                        description="Раньше было лучше, но наш бренд велик",
                        availability=True,
                        produced_country="us", produced_company="Winston")
            db.add(item)
            db.commit()
            link = await s3_create_download_link('shampan_detsk.jpg')
            item = Item(category_id=4, name="Детское Шампанское", price=1500, photo=link,
                        description="Лучший напиток на новый год, даже в 25",
                        availability=True,
                        produced_country="ru", produced_company="Буратино")
            db.add(item)
            db.commit()
            link = await s3_create_download_link('cola_2l.jpg')
            item = Item(category_id=4, name="Кола 2л", price=800, photo=link,
                        description="Промываем машины и желудки еще с 90-х",
                        availability=True,
                        produced_country="kz", produced_company="Coca Cola")
            db.add(item)
            db.commit()
            link = await s3_create_download_link('moloko_moe_25.jpg')
            item = Item(category_id=6, name="Молоко 6.2%", price=890, photo=link,
                        description="Это классика",
                        availability=True,
                        produced_country="kz", produced_company="Мое")
            db.add(item)
            db.commit()
            link = await s3_create_download_link('ya4a.jpg')
            item = Item(category_id=6, name="Яица С2 20шт", price=800, photo=link,
                        description="Мы любим всмятку, а вы?",
                        availability=True,
                        produced_country="kz", produced_company="Курочка Ряба")
            db.add(item)
            db.commit()
            link = await s3_create_download_link('sazan.jpg')
            item = Item(category_id=7, name="Сазан весовой", price=1200, photo=link,
                        description="Хороший и свежий",
                        availability=True,
                        produced_country="ru", produced_company="Лавка дяди Заура")
            db.add(item)
            db.commit()
            link = await s3_create_download_link('karas.jpg')
            item = Item(category_id=7, name="Карась весовой", price=700, photo=link,
                        description="Очень вкусно, когда денег мало",
                        availability=True,
                        produced_country="kz", produced_company="Лавка дяди Заура")
            db.add(item)
            db.commit()
            link = await s3_create_download_link('pirozhki.jpg')
            item = Item(category_id=8, name="Пирожки 1шт", price=150, photo=link,
                        description="Ешь много, а то будешь худой и слабый",
                        availability=True,
                        produced_country="kz", produced_company="Сара")
            db.add(item)
            db.commit()
            link = await s3_create_download_link('sosiska_v_teste.jpg')
            item = Item(category_id=8, name="Сосика в тесте 1шт", price=250, photo=link,
                        description="Для тех, кому пирожков мало",
                        availability=True,
                        produced_country="kz", produced_company="Сара")
            db.add(item)
            db.commit()
            link = await s3_create_download_link('belarus_kolbasa.jpg')
            item = Item(category_id=9, name="Белорусская колбаса весовая", price=4000, photo=link,
                        description="Дорого, но за то какое качества Беларуси",
                        availability=True,
                        produced_country="by", produced_company="Запасы беларуса")
            db.add(item)
            db.commit()
            link = await s3_create_download_link('tushenka_belarus.jpg')
            item = Item(category_id=9, name="Говяжья тушенка", price=1500, photo=link,
                        description="За такую тушенку можно и корову завалить",
                        availability=True,
                        produced_country="by", produced_company="Запасы беларуса")
            db.add(item)
            db.commit()
            link = await s3_create_download_link('baton.jpg')
            item = Item(category_id=10, name="Батон", price=300, photo=link,
                        description="Обычный батон",
                        availability=True,
                        produced_country="kz", produced_company="Цесна")
            db.add(item)
            db.commit()
            link = await s3_create_download_link('baget.jpg')
            item = Item(category_id=10, name="Багет", price=330, photo=link,
                        description="Хороший французский багет",
                        availability=True,
                        produced_country="kz", produced_company="Романовский продукт")
            db.add(item)
            db.commit()
            link = await s3_create_download_link('gurman_pelmen.jpg')
            item = Item(category_id=11, name="Пельмени 400г", price=600, photo=link,
                        description="Лучшая еда для студента",
                        availability=True,
                        produced_country="kz", produced_company="Гурман")
            db.add(item)
            db.commit()
            link = await s3_create_download_link('gurman_varenik.jpg')
            item = Item(category_id=11, name="Вареники 500г", price=400, photo=link,
                        description="Лучшая еда для студента",
                        availability=True,
                        produced_country="kz", produced_company="Гурман")
            db.add(item)
            db.commit()
            link = await s3_create_download_link('krabovie_palki_vici.jpg')
            item = Item(category_id=11, name="Крабовые палочки 200г", price=1000, photo=link,
                        description="Как настоящий!",
                        availability=True,
                        produced_country="lt", produced_company="Вичи")
            db.add(item)
            db.commit()
            return 200
        except:
            return 500
    else:
        return 500
