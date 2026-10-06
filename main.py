from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Model untuk data input
class Mahasiswa(BaseModel):
    nama: Optional[str] = None
    alamat: Optional[str] = None
    ipk: Optional[float] = None
    semester: Optional[int] = None
    hobi: Optional[str] = None

#simulasi database sederhana
mahasiswa_db = {}

#ROOT
@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

#create (POST)
@app.post("/mahasiswa/{mahasiswa_id}", status_code=201)
def create_mahasiswa(mahasiswa_id: int, mahasiswa: Mahasiswa):
    if mahasiswa_id in mahasiswa_db:
        raise HTTPException(status_code=400, detail="Mahasiswa already exists")
    mahasiswa_db[mahasiswa_id] = mahasiswa.model_dump()
    return {"message": "Mahasiswa created successfully", "mahasiswa_id": mahasiswa_id, "mahasiswa": mahasiswa_db[mahasiswa_id]}

# READ ALL (GET)
@app.get("/mahasiswa")
async def read_all_mahasiswa():
    return {"total": len(mahasiswa_db), "mahasiswa": mahasiswa_db}

# READ (GET)
@app.get("/mahasiswa/{mahasiswa_id}")
async def read_mahasiswa(mahasiswa_id: int):
    if mahasiswa_id not in mahasiswa_db:
        raise HTTPException(status_code=404, detail="Mahasiswa not found")
    return {"mahasiswa_id": mahasiswa_id, "mahasiswa": mahasiswa_db[mahasiswa_id]}

# UPDATE (PUT)
@app.put("/mahasiswa/{mahasiswa_id}")
async def update_mahasiswa(mahasiswa_id: int, mahasiswa: Mahasiswa):
    if mahasiswa_id not in mahasiswa_db:
        raise HTTPException(status_code=404, detail="Mahasiswa not found")
    mahasiswa_db[mahasiswa_id] = mahasiswa.model_dump()
    return {"message": "Mahasiswa updated successfully", "mahasiswa_id": mahasiswa_id, "mahasiswa": mahasiswa_db[mahasiswa_id]}

# DELETE (DELETE)
@app.delete("/mahasiswa/{mahasiswa_id}")
async def delete_mahasiswa(mahasiswa_id: int):
    if mahasiswa_id not in mahasiswa_db:
        raise HTTPException(status_code=404, detail="Mahasiswa not found")
    del mahasiswa_db[mahasiswa_id]
    return {"message": "Mahasiswa deleted successfully", "mahasiswa_id": mahasiswa_id}