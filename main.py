from fastapi import FastAPI
from services import create_db
from routes import user, token, mlmodels
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
create_db()
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(token.router)
app.include_router(mlmodels.router)
