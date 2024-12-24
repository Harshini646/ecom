from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from .routers import cart, orders
from .models.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uvicorn


app = FastAPI()

app.include_router(cart.router, prefix="/ecomm", tags=["Cart"])
app.include_router(orders.router, prefix="/ecomm", tags=["Order"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the E-commerce API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)