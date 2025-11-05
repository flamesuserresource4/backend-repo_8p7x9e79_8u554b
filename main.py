import os
from typing import List, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Task

app = FastAPI(title="Supply Chain Task & Workflow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Helpers
class JSONEncoder:
    @staticmethod
    def encode_doc(doc: dict) -> dict:
        if not doc:
            return doc
        d = {**doc}
        if "_id" in d and isinstance(d["_id"], ObjectId):
            d["id"] = str(d.pop("_id"))
        # Convert datetime to ISO strings
        for k, v in list(d.items()):
            if hasattr(v, 'isoformat'):
                try:
                    d[k] = v.isoformat()
                except Exception:
                    pass
        return d


@app.get("/")
async def root():
    return {"message": "Supply Chain Task & Workflow API running"}


@app.get("/test")
async def test_database():
    status = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "❌ Not Set",
        "database_name": "❌ Not Set",
        "collections": [],
    }
    try:
        if db is not None:
            status["database"] = "✅ Connected"
            status["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            status["database_name"] = db.name
            try:
                status["collections"] = db.list_collection_names()
            except Exception as e:
                status["collections"] = [f"error: {str(e)[:80]}"]
        else:
            status["database"] = "❌ Not Connected"
    except Exception as e:
        status["database"] = f"❌ Error: {str(e)[:80]}"
    return status


# Tasks Endpoints
@app.get("/api/tasks")
async def list_tasks() -> List[Any]:
    try:
        docs = get_documents("task", {}, None)
        return [JSONEncoder.encode_doc(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/tasks", status_code=201)
async def create_task(task: Task) -> dict:
    try:
        new_id = create_document("task", task)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
