from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.user import User as UserSchema
from app.schemas.user import UserCreate, UserUpdate
from app.crud.crud_user import user

router = APIRouter()

@router.get("/", response_model=List[UserSchema])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    全ユーザーを取得
    """
    users = user.get_multi(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=UserSchema)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    """
    新規ユーザーを作成
    """
    db_user = user.get_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="このメールアドレスは既に登録されています",
        )
    return user.create(db, obj_in=user_in)

@router.get("/{user_id}", response_model=UserSchema)
def read_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    特定のユーザーを取得
    """
    db_user = user.get(db, id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="ユーザーが見つかりません",
        )
    return db_user

@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    ユーザー情報を更新
    """
    db_user = user.get(db, id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="ユーザーが見つかりません",
        )
    return user.update(db, db_obj=db_user, obj_in=user_in)

@router.delete("/{user_id}", response_model=UserSchema)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    ユーザーを削除
    """
    db_user = user.get(db, id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="ユーザーが見つかりません",
        )
    return user.remove(db, id=user_id)
