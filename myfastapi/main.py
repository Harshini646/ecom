from fastapi import FastAPI
from .routers import cart, orders
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(cart.router, prefix="/ecomm", tags=["Cart"])
app.include_router(orders.router, prefix="/ecomm", tags=["Order"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the E-commerce API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
