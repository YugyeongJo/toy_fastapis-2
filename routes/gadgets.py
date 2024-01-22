from fastapi import APIRouter
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request


router = APIRouter()

templates = Jinja2Templates(directory="templates/")

@router.get("/buttons", response_class=HTMLResponse) # 펑션 호출 방식
async def buttons(request:Request):
    return templates.TemplateResponse(name="gadgets/buttons.html", context={'request':request})

@router.get("/Cards")
# request = Request(quer)
async def Cards(request:Request):
    return templates.TemplateResponse(name="gadgets/Cards.html", context={'request':request})

@router.post("/Cards")
async def Cards_post(request:Request):
    form_datas = await request.form()
    return templates.TemplateResponse(name="gadgets/Cards.html", context={'request':request})

@router.get("/colors", response_class=HTMLResponse)
async def colors(request:Request):
    return templates.TemplateResponse(name="gadgets/colors.html", context={'request':request})

@router.get("/container", response_class=HTMLResponse)
async def container(request:Request):
    return templates.TemplateResponse(name="gadgets/container.html", context={'request':request})
