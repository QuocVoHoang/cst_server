from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dinic import dinic_main_function

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],  
  allow_headers=["*"],  
)

class StringData(BaseModel):
  start_location_name: str
  end_location_name: str
  vehicle: str

@app.get("/")
async def mock_get():
  return {"message": "Hello from FastAPI"}

@app.post("/")
async def calculate_maxflow(data: StringData):  
  maxFlow = dinic_main_function(
    vehicle=data.vehicle,
    start_location_name=data.start_location_name, 
    end_location_name=data.end_location_name
  )
  if data.start_location_name == data.end_location_name: 
    return {"maxFlow": 0}
  else:
    maxFlow = int(maxFlow)
    return {"maxFlow": maxFlow}
  
# uvicorn main:app --host 0.0.0.0 --port 8000

