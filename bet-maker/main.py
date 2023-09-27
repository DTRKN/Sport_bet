from fastapi import FastAPI, APIRouter
from routers.bet import router
import uvicorn

app = FastAPI()
main_router = APIRouter()
main_router.include_router(router, prefix='/bet-maker', tags=['bet-maker'])
app.include_router(main_router)

def start_server():
    print('Starting Server...')

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        log_level="debug",
        reload=True,
    )

if __name__ == '__main__':
    start_server()