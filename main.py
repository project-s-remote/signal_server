from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sockets import sio_app
import uvicorn
from mongodb import remote_collection

from bson import ObjectId
from pydantic import BaseModel, ConfigDict

BaseModel.model_config["json_encoders"] = {ObjectId: lambda v: str(v)}

app = FastAPI()

# Mount the Socket.IO server as an ASGI app
app.mount("/ws", sio_app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/api/create/remote")
async def create_remote_id(request: Request):
    # 여기도 마찬가지로 랜덤오브제아이디 _id 받아 아이디 고정방식으로 갈 예정이다.
    body = await request.json()

    result = remote_collection.insert_one(body)
    inserted_id = result.inserted_id

    print(result)

    return str(inserted_id)


@app.get('/api/get/remote/{objid}')
async def get_remote(objid: str):
    result = remote_collection.find_one({"_id": ObjectId(objid)})
    result["_id"] = str(result.get("_id"))
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
