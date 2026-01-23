from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from test_runner import test_submission

app = FastAPI(title="BroCode Execution API")

class RunRequest(BaseModel):
    question_id: str  # e.g., "E01"
    code: str

@app.post("/run")
async def run_code(payload: RunRequest):
    
    result = test_submission(payload.question_id, payload.code)
    
    if "error" in result and result["status"] == "FAIL" and "Unknown question ID" in result.get("error", ""):
         raise HTTPException(status_code=400, detail=result["error"])
         
    return result

if __name__ == "__main__":
    import uvicorn
   
    uvicorn.run(app, host="0.0.0.0", port=8001)