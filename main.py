from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import random
import string

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

# TODO: use `Alembic` for initializing db
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def make_short_url() -> str:
    uniqueValues = string.ascii_letters + string.digits
    return ''.join(random.choices(uniqueValues, k=6))


@app.get("/")
async def read_root():
    return "Home page!"

# USER API


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=400, detail="User with such email already exists")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db=db, skip=skip, limit=limit)



# URL API


# @app.post("/shorturl", response_model=schemas.Url)
# def shorten_url(url: URL):
#     conn = sqlite3.connect('data/db.sqlite')
#     shortURL = make_short_url()
#     cursor = conn.cursor()
#     cursor.execute(
#         f'INSERT INTO urltable (shorturl, longurl) VALUES (\'{shortURL}\', \'{url.url}\')')
#     conn.commit()
#     conn.close()
#     return {"short_url": shortURL}


# @app.get("/shorturl")
# def read_all_urls():
#     conn = sqlite3.connect('data/db.sqlite')
#     cursor = conn.cursor()
#     cursor.execute(f'SELECT * FROM urltable')
#     resultList = cursor.fetchall()
#     conn.close()
#     return resultList


# @app.get("/shorturl/{shortURL}")
# def read_url(shortURL: str):
#     conn = sqlite3.connect('data/db.sqlite')
#     cursor = conn.cursor()
#     cursor.execute(
#         f'SELECT longurl FROM urltable WHERE shorturl=\'{shortURL}\'')
#     resultList = cursor.fetchall()
#     conn.close()
#     if len(resultList) == 0:
#         raise HTTPException(status_code=404, detail="URL not found")
#     elif len(resultList) != 1:
#         raise HTTPException(status_code=404, detail="Multiple URLs were found")
#     return RedirectResponse(resultList[0][0])
