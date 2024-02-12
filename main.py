from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

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


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# URL API


@app.post("/users/{user_id}/urls/", response_model=schemas.Url)
def create_url(user_id: int, url: schemas.UrlCreate, db: Session = Depends(get_db)):
    return crud.create_user_url(db=db, url=url, user_id=user_id)


@app.get("/urls/", response_model=list[schemas.Url])
def read_urls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_urls(db=db, skip=skip, limit=limit)


@app.get("/urls/{encoded_url}", response_model=schemas.Url)
def read_url(encoded_url: str, db: Session = Depends(get_db)):
    return crud.get_url(db=db, encoded_url=encoded_url)
