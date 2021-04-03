from typing import Optional
import uvicorn

from fastapi import FastAPI,Depends
from pydantic import BaseModel
from routers import stripe,paypal
from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()

# CORS SETTING
origins = [
  "*",
  "http://localhost:3000",
  "http://localhost:8080",
  "http://localhost:3002",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
  name: str
  price: float
  is_offer: Optional[bool] = None


# include url here
app.include_router(stripe.router)
app.include_router(paypal.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.price, "item_id": item_id}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)