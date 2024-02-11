from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = str(hash(user.password))
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_url(db: Session, encoded_url: str):
    return db.query(models.Url).filter(models.Url.encoded_url == encoded_url).first()

def get_urls(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Url).offset(skip).limit(limit).all()

def create_user_url(db: Session, url: schemas.UrlCreate, user_id: int):
    db_url = models.Url(**url.model_dump(), owner_id = user_id)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url