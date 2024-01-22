from fastapi import APIRouter
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request


router = APIRouter()

templates = Jinja2Templates(directory="templates/")

@router.get("/forms", response_class=HTMLResponse) # 펑션 호출 방식
async def forms(request:Request):
    return templates.TemplateResponse(name="positionings/forms.html", context={'request':request})

@router.get("/grids", response_class=HTMLResponse)
async def grids(request:Request):
    return templates.TemplateResponse(name="positionings/grids.html", context={'request':request})

@router.get("/standards", response_class=HTMLResponse)
async def standards(request:Request):
    return templates.TemplateResponse(name="positionings/standards.html", context={'request':request})

@router.get("/tables", response_class=HTMLResponse)
async def tables(request:Request):
    return templates.TemplateResponse(name="positionings/tables.html", context={'request':request})