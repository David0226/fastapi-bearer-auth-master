from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email,
                          hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


''' dashboard '''


def get_dashboard(db: Session, dashboard_id: str):
    return db.query(models.Dashboard).filter(
        models.Dashboard.dashboard_id == dashboard_id).first()


def get_dashboards(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Dashboard).offset(skip).limit(limit).all()


def create_dashboard(db: Session, dashboard: schemas.DashboardCreate):
    db_dashboard = models.Dashboard(**dashboard.dict())
    db.add(db_dashboard)
    db.commit()
    db.refresh(db_dashboard)
    return db_dashboard


def update_dashboard(db: Session, dashboard: schemas.DashboardUpdate,
                     dashboard_id: str):
    db_dashboard = get_dashboard(db, dashboard_id)
    if db_dashboard is None:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    # db_dashboard.dashboard_name = dashboard.dashboard_name
    db_dashboard.dashboard_json = dashboard.dashboard_json
    db.commit()
    db.refresh(db_dashboard)
    return db_dashboard


def delete_dashboard(db: Session, dashboard_id: str):
    db_dashboard = get_dashboard(db, dashboard_id)
    if db_dashboard is None:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    db.delete(db_dashboard)
    db.commit()
    return db_dashboard
