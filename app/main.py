from fastapi import FastAPI
from app.users.router import router_auth, router_users
from app.images.router import router as router_images
from app.products.routers import router as router_products
from app.variations.router import router as router_variations
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="E-Синергия")


# Включение основных роутеров
app.include_router(router_auth)
app.include_router(router_users)
#app.include_router(router_products)

#app.include_router(router_variations)
#app.include_router(router_images)

origins = [
    # 3000 - порт, на котором работает фронтенд на React.js
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)
app.mount("/static", StaticFiles(directory="app/static"), "static")