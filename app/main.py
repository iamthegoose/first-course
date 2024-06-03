from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import HTTPException
from app.services.connection import SessionFactory
from app.services.security import get_password_hash, verify_password, create_access_token, get_current_user_from_token, get_current_user

# repository
from app.repositoryuser import UserRepository
from app.repositoryflat import FlatRepository

# types & models
from app.services.models.user import User
from app.services.models.flat import Flat
from app.services.types.flatfilters import FlatFilters
from app.services.models.requests import UserSigninRequest, UserSignupRequest, FlatCreateRequest

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/front/static",
          html=True), name="static")

templates = Jinja2Templates(directory="app/front/html")

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index_file(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/signup")
def signup(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@app.get("/profile-red")
def profile_red(request: Request):
    return templates.TemplateResponse("profile-red.html", {"request": request})


@app.get("/profile")
def get_profile(request: Request, token: str = Depends(get_current_user)):
    print(token)
    if token:
        current_user = get_current_user_from_token(token)
        with SessionFactory() as sess:
            flatRepository = FlatRepository(sess)
            user_flats = flatRepository.get_flats_by_user_id(current_user.id)
        return templates.TemplateResponse("profile.html", {"request": request, "flats": user_flats})
    else:
        return templates.TemplateResponse("login.html", {"request": request})


@app.get("/rent")
def rent(request: Request):
    with SessionFactory() as sess:
        flatRepository = FlatRepository(sess)
        flats = flatRepository.get_all_flats()
    return templates.TemplateResponse("flats.html", {"request": request, "flats": flats})


@app.get("/create-flats")
def create_flats(request: Request):
    return templates.TemplateResponse("create-flats.html", {"request": request})


@app.post("/user/signup")
def signup_user(user_request: UserSignupRequest, request: Request):
    with SessionFactory() as sess:
        userRepository = UserRepository(sess)
        db_user = userRepository.get_user_by_email(user_request.email)

        if db_user:
            return templates.TemplateResponse("registration.html", {"request": request, "message": "Користувач з такою поштою вже існує!"})

        signup = User(
            email=user_request.email,
            name=user_request.name,
            surname=user_request.surname,
            password=get_password_hash(user_request.password)
        )
        success = userRepository.create_user(signup)

        token = create_access_token(sess, user_request.email)

        return JSONResponse(status_code=201, content={"message": "Користувач створений успішно!", "token": token})



@app.post("/user/signin")
def signin_user(user_request: UserSigninRequest, request: Request):
    with SessionFactory() as sess:
        userRepository = UserRepository(sess)
        db_user = userRepository.get_user_by_email(user_request.email)
        if not db_user:
            return JSONResponse(status_code=400, content={"message": "Користувача з такою поштою не існує!"})

        if verify_password(user_request.password, db_user.password):
            token = create_access_token(sess, user_request.email)
            return JSONResponse(status_code=200, content={"message": "Успішний вхід", "token": token})

        return JSONResponse(status_code=400, content={"message": "Неправильний пароль!"})


@app.get("/success", response_class=HTMLResponse)
def success_page(request: Request, token: str):
    return templates.TemplateResponse("index.html", {"request": request, "token": token})


@app.post("/user/create-flat")
def create_flat(flat_request: FlatCreateRequest, current_user: User = Depends(get_current_user_from_token)):
    with SessionFactory() as sess:
        flatRepository = FlatRepository(sess)
        new_flat = Flat(
            name=flat_request.name,
            location=flat_request.location,
            description=flat_request.description,
            area=int(flat_request.area),
            price=int(flat_request.price),
            rooms=int(flat_request.rooms),
            user_id=current_user.id
        )
        success = flatRepository.create_flat(new_flat)
        if success:
            return JSONResponse(status_code=201, content={"message": "Квартира створена успішно"})
        else:
            raise HTTPException(
                status_code=500, detail="Помилка при створенні квартири")


@app.post("/user/flats", response_class=HTMLResponse)
def flats(request: Request, filters: FlatFilters):
    filter_dict = {}

    if filters.area_from is not None:
        filter_dict["area_min"] = filters.area_from
    if filters.area_to is not None:
        filter_dict["area_max"] = filters.area_to

    if filters.price_from is not None:
        filter_dict["price_min"] = filters.price_from
    if filters.price_to is not None:
        filter_dict["price_max"] = filters.price_to

    if filters.rooms is not None:
        filter_dict["rooms"] = filters.rooms

    with SessionFactory() as sess:
        flatRepository = FlatRepository(sess)
        flats = flatRepository.get_all_flats(filters=filter_dict)

    return templates.TemplateResponse("flats.html", {"request": request, "flats": flats})


logging.basicConfig(level="DEBUG")
