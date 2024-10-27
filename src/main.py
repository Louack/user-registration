import uvicorn
from fastapi import FastAPI

from src.auth.adapters.fastapi.rest_routes import router as user_router
from src.fastapi_exceptions_handlers import register_exception_handlers

app = FastAPI()
app.include_router(user_router)
register_exception_handlers(app)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
