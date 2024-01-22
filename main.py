from fastapi import FastAPI
app = FastAPI()

from databases.connections import Settings
settings = Settings()
@app.on_event("startup")
async def init_db():
    await settings.initialize_database()

from routes.gadgets import router as event_router
from routes.positionings import router as second_router
from routes.users import router as users_router
from routes.homes import router as home_router
from routes.events_api import router as events_api_router
from routes.users_api import router as users_api_router

from fastapi import Request
from fastapi.templating import Jinja2Templates
app.include_router(event_router, prefix="/gadget")
app.include_router(second_router, prefix="/positioning")
app.include_router(users_router, prefix="/users")
app.include_router(home_router, prefix="/home")
app.include_router(events_api_router, prefix="/events_api")
app.include_router(users_api_router, prefix="/users_api")



# html 들이 있는 폴더 위치
templates = Jinja2Templates(directory="templates/")

from fastapi.middleware.cors import CORSMiddleware
# No 'Access-Control-Allow-Origin'
# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 접근 가능한 도메인만 허용하는 것이 좋습니다.
    allow_methods=["*"],
    allow_headers=["*"],
)

# 클라이언트가 바라보는 위치와 내부 서버에서 바라보는 위치를 일치시켜주는 것
# fastapi의 directory를 넣는 곳 + 앞에 CL위치를 넣어줌
  # example
  # from fastapi.staticfiles import StaticFiles
  # app.mount("/static", StaticFiles(directory="static"), name="static")
# url 경로, 자원의 물리 경로(directory), 프로그래밍 측면 모두 맞춰주기
from fastapi.staticfiles import StaticFiles
app.mount("/css", StaticFiles(directory="resources\\css\\"), name="static_css")
app.mount("/images", StaticFiles(directory="resources/images/"), name="static_image")

@app.get("/")
async def root(Request:Request):
    # return {"message": "jisu World"}
    return templates.TemplateResponse("main.html",{'request':Request})

@app.post("/")
async def root(Request:Request):
    # return {"message": "jisu World"}
    return templates.TemplateResponse("main.html",{'request':Request})

