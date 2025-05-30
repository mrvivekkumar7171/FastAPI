from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello, World!"}

@app.get("/greet/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}!"}
# to run the app, use the command:
# uvicorn main:app --reload

# reload will automatically reload the server when you make changes to the code
# http://127.0.0.1:8000/docs to see the API documentation