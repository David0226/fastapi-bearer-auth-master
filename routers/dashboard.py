from typing import List
from fastapi import APIRouter

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from database import db_conn

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    responses={404: {"description": "Not found"}},
)


router.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(db_conn.get_db())):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(db_conn.get_db())):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(db_conn.get_db())):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id: int,
                         item: schemas.ItemCreate,
                         db: Session = Depends(db_conn.get_db())):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@router.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(db_conn.get_db())):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@router.get("/dashboards/", response_model=List[schemas.Dashboard])
def read_dashboards(skip: int = 0,
                    limit: int = 100,
                    db: Session = Depends(db_conn.get_db())):
    dashboards = crud.get_dashboards(db, skip=skip, limit=limit)
    return dashboards


@router.get("/dashboards/{dashboard_id}", response_model=schemas.Dashboard)
def read_dashboard(dashboard_id: str, db: Session = Depends(db_conn.get_db())):
    db_dashboard = crud.get_dashboard(db, dashboard_id=dashboard_id)
    if db_dashboard is None:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return db_dashboard


@router.post("/dashboards/", response_model=schemas.Dashboard)
def create_dashboard(dashboard: schemas.DashboardCreate,
                     db: Session = Depends(db_conn.get_db())):
    return crud.create_dashboard(db=db, dashboard=dashboard)


@router.put("/dashboards/{dashboard_id}", response_model=schemas.Dashboard)
def update_dashboard(dashboard_id: str,
                     dashboard: schemas.DashboardUpdate,
                     db: Session = Depends(db_conn.get_db())):
    return crud.update_dashboard(db=db,
                                 dashboard_id=dashboard_id,
                                 dashboard=dashboard)


@router.delete("/dashboards/{dashboard_id}", response_model=schemas.Dashboard)
def delete_dashboard(dashboard_id: str, db: Session = Depends(db_conn.get_db())):
    return crud.delete_dashboard(db=db, dashboard_id=dashboard_id)