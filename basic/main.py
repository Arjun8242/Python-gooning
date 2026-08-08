from fastapi import FastAPI
# pyrefly: ignore [missing-import]
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, welcome to the basic FastAPI server!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
