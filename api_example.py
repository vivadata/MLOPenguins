from fastapi import FastAPI
from fastapi.requests import Request
from pydantic import BaseModel

class Student(BaseModel):
    id: int
    name: str
    age: int

student = Student(id=1, name="Aloys", age=30)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/hello")
def say_hello(student: Student):
    return student

@app.get("/count")
def count_hello(num: int):
    return {"Hello": "World " * num}


global count
count = 0
@app.get("/counter")
def counter():
    global count
    count += 1
    return {"count": count}
