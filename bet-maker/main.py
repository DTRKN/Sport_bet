from fastapi import FastAPI, APIRouter
from routers.bet import router
import uvicorn

app = FastAPI()
main_router = APIRouter()
main_router.include_router(router, prefix='/bet-maker', tags=['bet-maker'])
app.include_router(main_router)

if __name__ == '__main__':
    config = uvicorn.Config("main:app", port=5000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    server.run()