from fastapi import FastAPI
from todo.routes import main_router

app = FastAPI(
    title='Todo List Manager',
    version='0.1.0',
    description='A simple **todo list** manager API.'
)


@app.get('/')
def hello():
    """A simple entrypoint of our API!"""
    return {'mesage': 'Hello, World!'}


app.include_router(main_router)
