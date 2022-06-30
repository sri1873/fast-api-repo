import typing as t
from datetime import date
from typing import List
from pydantic import BaseModel

from model import AssetsModel, UserModel


# PostModel schema takes input for a post method

class Login(BaseModel):
    email_id: str
    password: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username: str


class CreateUser(BaseModel):
    role: str
    email_id: str
    password: str
    first_name: str
    last_name: str
    date_of_birth: date
    phone_number: int
    address: str
    city: str
    state: str
    country: str

    class Config:
        orm_mode = True


class UserDetails(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    phone_number: int
    address: str
    city: str
    state: str
    country: str

    class Config:
        orm_mode = True


class PostAttendance(BaseModel):
    in_time: bool

    class Config:
        orm_mode = True


class PostAssets(BaseModel):
    laptop_id: str
    phone_id: str
    sim_number: int
    benefits: str
    email_id: str

    class Config:
        orm_mode = True


class PostProject(BaseModel):
    project_id: int
    project_description: str
    duration: int
    start_date: date
    end_date: date

    class Config:
        orm_mode = True


class CreateTeam(BaseModel):
    project_id: int
    email_id: str

    class Config:
        orm_mode = True


class JoinResult(BaseModel):
    results: t.List[t.Dict[PostAssets, CreateUser]]

    class Config:
        orm_mode = True

# Response Models schema tells how output must be fetched in a get method
