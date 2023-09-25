from fastapi import FastAPI, APIRouter
from routers.send_data import router
import uvicorn

app = FastAPI()
main_router = APIRouter()
main_router.include_router(router, prefix='/line-prov', tags=['line-prov'])
app.include_router(main_router)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
