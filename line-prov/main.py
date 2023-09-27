from fastapi import FastAPI, APIRouter
from routers.send_data import router
from config import *
import uvicorn

app = FastAPI()
main_router = APIRouter()
main_router.include_router(router, prefix='/line-prov', tags=['line-prov'])
app.include_router(main_router)

def start_server():
    print('Starting Server...')

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        log_level="debug",
        reload=True,

    )

if __name__ == '__main__':
    start_server()
