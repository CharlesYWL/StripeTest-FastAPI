from fastapi import APIRouter, HTTPException
# from ..dependencies import get_token_header
import json
import os
from pydantic import BaseModel
from typing import Optional, List

# stripe setting
import stripe

stripe.api_key = "sk_test_51IZipEIbg2Wdh6h2bgIimgX4iUHfrfdQZeVMqdtf41RYjaMwiYCCfLIaElbT0xpxY51Lk7ZVquVIAQ7LcsdQwnQ600ArautoBa"

router = APIRouter(
  prefix="/stripe",
  tags=["stripe"],
  # dependencies=[Depends(get_token_header)],
  responses={404: {"details": "Not found"}},
)


class Item(BaseModel):
  id: str
  quantity: Optional[int] = 1
  class Config:
    schema_extra = {
      "example":{
        "id":"SampleTest0",
        "quantity":1
      }
    }

class Items(BaseModel):
  items: List[Item] = []

  class Config:
    schema_extra = {
      "items":[
        {"id":"SampleTest0","quantity":1},
        {"id":"SampeTest1","quantity":2}
      ]
    }

def calculate_order_amount(items):
  # Replace this constant with a calculation of the order's amount
  # Calculate the order total on the server to prevent
  # people from directly manipulating the amount on the client
  return 0


YOUR_CHECKOUTURL = 'https://payment-ui-nextjs-q7wgrl1si-charlesywl.vercel.app/order'


DefaultItems = [
{ "name":"sampletest0" ,"data":{
  'currency': 'usd',
  'unit_amount': 500,
  'product_data': {
    'name': 'SampleTest0',
    'images': ['https://i.imgur.com/u1R691i.png'],
  }},},
{ "name":"sampletest1", "data":{
           'currency': 'usd',
           'unit_amount': 1500,
           'product_data': {
             'name': 'SampeTest1',
             'images': ['https://i.imgur.com/57eqR91.jpg'],
           }}},
{ "name":"sampletest2", "data":{
           'currency': 'usd',
           'unit_amount': 3500,
           'product_data': {
             'name': 'SampeTest3',
             'images': ['https://i.imgur.com/IX981c4.png'],
           }
         }},
]
EmptyItem = {
           'currency': 'usd',
           'unit_amount': 0,
           'product_data': {
             'name': 'EmptyItem',
             'images': ['https://i.imgur.com/IX981c4.png'],
           }
         }


def find_index_by_key(list, key, target):
  return [x[key] for x in list].index(target)


@router.post("/")
def test(item:Item):
  return (item)
  # return ({"detail":"StripeRoute Test"})

@router.post("/create-checkout-session-single")
def create_checkout_session_single(item:Item):
  new_line_items = []
  item.id = item.id.lower()
  if item.id not in [x['name'] for x in DefaultItems]:
    raise HTTPException(status_code=404, detail="Item not found")
  new_line_items.append(
    {
      'price_data':DefaultItems[find_index_by_key(DefaultItems,'name',item.id)]['data'],
      'quantity': item.quantity or 1,
    }
  )
  try:
    checkout_session = stripe.checkout.Session.create(
      payment_method_types=['card'],
      line_items=new_line_items,
      mode='payment',
      success_url=YOUR_CHECKOUTURL + '?success=true',
      cancel_url=YOUR_CHECKOUTURL + '?canceled=true',
    )
    return ({'id': checkout_session.id})
  except Exception as e:
    raise HTTPException(status_code=404, detail="some error on server side")


@router.post("/create-checkout-session")
async def create_checkout_session(items:Items):
  line_items = []
  for item in items.items:
    qua = item['quantity'] or 1
    line_item = {
      "price_data": items[item.id],
      "quantity":qua
    }
    line_items.append(line_item)
  try:
    checkout_session = stripe.checkout.Session.create(
      payment_method_types=['card'],
      line_items=line_items,
      mode='payment',
      success_url=YOUR_CHECKOUTURL + '?success=true',
      cancel_url=YOUR_CHECKOUTURL + '?canceled=true',
    )
    return ({'id': checkout_session.id})
  except Exception as e:
    raise HTTPException(status_code=404, detail="some error on server side")

@router.get("/get-goods")
def get_item():
  return ({"itemList":DefaultItems})

@router.get("/get-goods/{item_id}")
def get_single_item(item_id:str):
  item_id = item_id.lower()
  if not item_id or (item_id not in [x['name'] for x in DefaultItems]):
    return HTTPException(detail="no such items", status_code=404)
  return DefaultItems[find_index_by_key(DefaultItems,'name',item_id)]