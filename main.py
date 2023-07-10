from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

import models
from database import engine, SessionLocal
from models import Inventory
from datetime import datetime, date


app = FastAPI()


models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/inventario")
async def get_all(db: db_dependency):
    return db.query(Inventory).order_by(Inventory.id).all()


class InventoryRequest(BaseModel):
    product_id: str = Field()
    quantity: int = Field()
    date: str = Field()
    time: str = Field()


@app.post("/add-register")
async def add_register(db: db_dependency, inv_request: InventoryRequest):
    inv_model = Inventory(**inv_request.dict())
    db.add(inv_model)
    db.commit()


@app.put("/edit/{id_inv}")
async def edit_register(db: db_dependency, id_inv: int, inv_request: InventoryRequest):
    inv_model = db.query(Inventory).filter(Inventory.id == id_inv).first()
    inv_model.product_id = inv_request.product_id
    inv_model.quantity = inv_request.quantity
    inv_model.date = inv_request.date
    inv_model.time = inv_request.time

    db.add(inv_model)
    db.commit()

