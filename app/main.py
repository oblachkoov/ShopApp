from fastapi import FastAPI


from app.auth.routers import router as auth_router

app = FastAPI()

app.include_router(auth_router)





# Sam_20081619
