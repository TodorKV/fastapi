from fastapi import FastAPI
from pydantic import BaseModel
import wtf

app = FastAPI()

class Msg(BaseModel):
    msg: str


@app.get("/")
async def root():
    return {"message": "ask me about covid19"}

@app.get("/ask/{question}")
async def askMe(question):
    return wtf.predict(question=question)