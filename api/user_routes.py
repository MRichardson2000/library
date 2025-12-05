from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from data.database.dbconn import load_env, get_engine, get_session
from src.repositories.user_repository import UserRepository
from src.services.user_services import UserServices
from pydantic import BaseModel
from typing import Generator

router = APIRouter()

class UserResponse(BaseModel):
    first_name: str
    email: str

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email_address: str
    phone_number: int

def get_db() -> Generator[Session, None, None]:
    db_details = load_env()
    engine = get_engine(db_details)
    SessionLocal = get_session(engine)
    with SessionLocal() as session:
        yield session

@router.post("/users", response_model=UserResponse)
def create_user(user_data: UserCreate, session: Session = Depends(get_db)):
        repo = UserRepository(session)
        service = UserServices(repo)
        user = service.create_user(
            user_data.first_name,
            user_data.last_name,
            user_data.email_address,
            user_data.phone_number
        )
        return UserResponse(first_name=user.first_name, email=user.email_address)