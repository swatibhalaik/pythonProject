from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient

app = FastAPI()


DB = "api_test"


EMP_COLLECTION = "emp"


class Info(BaseModel):
    name: str
    emp_id: int
    loc: str
    is_working_from_home: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Message": "Hello Employee"}


@app.post("/Info/")
def create_item(info: Info):
    with MongoClient() as client:
        msg_collection = client[DB][EMP_COLLECTION]
        result = msg_collection.insert_one(info.dict())
        ack = result.acknowledged
        return {"insertion": ack}


@app.get("/Info/{emp_id}")
def read_item(emp_id: int):
    with MongoClient() as client:
        msg_collection = client[DB][EMP_COLLECTION]
        result = msg_collection.find({"emp_id": emp_id})
        ack = result.acknowledged
        return ({Info.dict()} , ack)


@app.put("/Info/{emp_id}")
def update_info(emp_id: int, loc: str):
    with MongoClient() as client:
        msg_collection = client[DB][EMP_COLLECTION]
        result = msg_collection.update({"emp_id": emp_id}, {"loc": loc})
        ack = result.acknowledged
        return {"Updated": ack}

