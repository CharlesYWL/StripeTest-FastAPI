from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter(
  prefix="/paypal",
  tags=["paypal"],
  # dependencies=[Depends(get_token_header)],
  responses={404: {"details": "Not found"}},
)

class Order(BaseModel):
  orderID:str
  class Config:
    schema_extra = {
      "example":{
        "orderId":"xxxxxxxxxxx"
      }
    }


@router.post('/paypal-transaction-complete')
def get_order(order:Order):
  print(order)
  if (not order) or (order == ""):
    raise HTTPException(status_code=404, detail="OrderId not found")
  else:
    return(order)
