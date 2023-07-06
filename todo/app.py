from fastapi import FastAPI

app = FastAPI(
    title='Todo List Manager',
    version='0.1.0',
    description='A simple **todo list** manager API.'
)


@app.get('/')
def hello():
    """A simple entrypoint of our API!"""
    return {'mesage': 'Hello, World!'}
