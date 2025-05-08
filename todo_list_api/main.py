from fastapi import FastAPI,HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from database import Base
import schemas
import auth
from auth import *
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

app=FastAPI()
Base.metadata.create_all(bind=engine)
detail="Task not found"

class Task(BaseModel):
    name: str
    completed: bool = False

def get_db():
    db=SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependancy=Annotated[Session,Depends(get_db)]

@app.post("/tasks")
async def add_task(task: Task, db:db_dependancy):
    db_task=models.Tasks(task=task.name,completed=task.completed)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/{task_id}")
async def get_task(task_id: int, db:db_dependancy):
    db_task=db.query(models.Tasks).filter(models.Tasks.id==task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail=detail)
    return db_task

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task_update: schemas.TaskUpdate,db:db_dependancy):
    db_task=db.query(models.Tasks).filter(models.Tasks.id==task_id).first()
    if not db_task: raise HTTPException(status_code=404, detail=detail)
    for field, value in task_update.dict(exclude_unset=True).items():setattr(db_task,field,value)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db:db_dependancy):
    db_task=db.query(models.Tasks).filter(models.Tasks.id==task_id).first()
    if not db_task: raise HTTPException(status_code=404, detail=detail)
    db.delete(db_task)
    db.commit()
    return {"message":"Task deleted successfully"}

@app.patch("/tasks/{task_id}/complete")
async def mark_complete(task_id: int, db:db_dependancy):
    db_task=db.query(models.Tasks).filter(models.Tasks.id==task_id).first()
    if not db_task: raise HTTPException(status_code=404, detail=detail)
    db_task.complete=True
    db.commit()
    return {"message":"Task completed"}

@app.post("/register",response_model=schemas.UserResponse)
async def register(user: schemas.UserCreate, db: db_dependancy):
    existing_user=db.query(models.User).filter(models.User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    hashed_password=auth.get_password_hash(user.password)
    db_user=models.User(email=user.email,hashed_password=hashed_password,is_active=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    if hasattr(schemas.UserResponse,'model_validate'):return schemas.UserResponse.model_validate(db_user)
    else: return schemas.UserResponse.from_orm(db_user)

@app.post("/login",response_model=schemas.Token)
async def login_for_access_token(db:db_dependancy,form_data: OAuth2PasswordRequestForm=Depends()):
    user=authenticate_user(db,email=form_data.username,password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-AUTHENTICATE":"Bearer"})
    token_expires=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRY_MINUTES)
    access_token=auth.create_access_token(data={"sub":user.email},expires=token_expires)
    return {"access_token":access_token,"token_type":"Bearer"}
