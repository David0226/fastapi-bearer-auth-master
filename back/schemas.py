from typing import List, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True


class DashboardBase(BaseModel):
    dashboard_id: str
    title: str
    description: Optional[str] = None
    dashboard_json: Optional[str] = None


class DashboardCreate(DashboardBase):
    pass


class DashboardUpdate(DashboardBase):
    pass


class Dashboard(DashboardBase):
    id: int

    class Config:
        orm_mode = True