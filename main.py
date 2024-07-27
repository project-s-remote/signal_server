from fastapi import FastAPI, Request, HTTPException
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
@app.get("/")
def home():
    return {"message": "Hello World!"}


@app.get("/api/empty_remote")
async def create_remote_id():

    result = remote_collection.insert_one({ "signal": None, "sid": None, "screen_id": None, "width": None, "height": None})
    inserted_id = result.inserted_id

    return str(inserted_id)

@app.put("/api/remote/{objid}")
async def create_remote_id(objid: str, request: Request):
    body = await request.json()
    
    # 객체 ID가 유효한지 확인
    if not ObjectId.is_valid(objid):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    # 업데이트할 데이터 준비
    update_data = { "$set": body }

    # 데이터베이스에서 업데이트
    result = remote_collection.update_one({ "_id": ObjectId(objid) }, update_data)

    # 업데이트 결과 확인
    if result.modified_count == 1:
        return {"message": "update 성공"}
    else:
        return {"message": "update 실패", "details": result.raw_result}


@app.get('/api/remote/{objid}')
async def get_remote(objid: str):
    result = remote_collection.find_one({"_id": ObjectId(objid)})
    result["_id"] = str(result.get("_id"))
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
