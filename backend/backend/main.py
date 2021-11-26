from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session


from backend import crud, models, schemas
from backend.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
    
app = FastAPI()
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    user = crud.create_user(db=db, user=user)
    
    return user

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

#informação do usuário
@app.get("/users/{user_id}", response_model=schemas.User)
def find_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id)

#editar usuário
@app.put("/users/{user_id}", response_model=schemas.User)
async def edit_user(user_id: int, new_value: schemas.UserEdit, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user:
        return crud.edit_user(db, user_id, new_value=new_value)
    
    raise HTTPException(status_code=400, detail="Usuário não existe")


@app.patch("/users/{user_id}", response_model=schemas.User)
async def edit_user(user_id: int, new_value: schemas.UserEdit, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user:
        return crud.edit_user(db, user_id, new_value=new_value)
    
    raise HTTPException(status_code=400, detail="Usuário não existe")

#medidas
@app.get("/measures/", response_model=List[schemas.Measure])
def read_measures(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_measures(db, skip=skip, limit=limit)
    return users


@app.post("/users/{user_id}/measures/", response_model=schemas.Measure)
def create_measure(user_id: int, measure: schemas.MeasureCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user:
        return crud.create_user_measure(db, measure, user_id)

    raise HTTPException(status_code=400, detail="Usuário inexistente")


@app.get("/users/{user_id}/measures/", response_model=List[schemas.Measure])
def get_user_measure(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user:
        return crud.get_user_measure(db, user_id)

    raise HTTPException(status_code=400, detail="Usuário não existe")