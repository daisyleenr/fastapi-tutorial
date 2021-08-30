from enum import Enum
from typing import Optional

from fastapi import FastAPI


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()
fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
]


@app.get("/models/{model_name}")
async def get_model(
    model_name: ModelName,
):  # Enum type으로 받는 경우 swagger에서 selector 제공
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/me")  # 동적 매개변수와 함께 사용 시 순서 중요
async def read_user_me():
    return {"user_id": "the corrent user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/items/{item_id}")
async def read_item(item_id: int):  # 타입 선언 시 자동 parsing 및 데이터 검증
    return {"item_id": item_id}


@app.get("/items/")
async def read_item_2(
    skip: int = 0, limit: int = 10
):  # 자동으로 쿼리 스트링 인식 ex) http://127.0.0.1:8000/items/?skip=0&limit=10
    # 쿼리를 필수로 만들고 싶은 경우 기본값 설정 X

    return fake_items_db[skip : skip + limit]


@app.get("/optional/{option_id}")
async def read_option(
    option_id: str, q: Optional[str] = None, short: bool = False
):  # optional parameter 사용 가능
    option = {"option_id": option_id}
    if q:
        option.update({"option_id": option_id, "q": q})
    if not short:  # bool 자동 형변환
        option.update(
            {
                "description": "This is an amazing item that has a long description."
            }
        )
    return option
