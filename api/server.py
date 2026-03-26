from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from modules.agents.agent_pipeline import run_case_pipeline

app = FastAPI()


class Document(BaseModel):
    type: str
    side: str
    content: str


class CaseRequest(BaseModel):
    case_id: str
    documents: List[Document]


@app.post("/case/run")
def run_case(req: CaseRequest):
    result = run_case_pipeline(req.case_id, [d.dict() for d in req.documents])
    return result

@app.get("/")
def root():
    return {"System": "GPT-OS Legal API Running"}
