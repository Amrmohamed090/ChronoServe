from fastapi import FastAPI

app = FastAPI()

@app.get("/test")
async def test():
    return {"message": "Service1 responding OK"}
