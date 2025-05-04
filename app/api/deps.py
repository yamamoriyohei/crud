from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.crud.crud_user import user

# 認証をオプションにする
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

def get_current_user(
    db: Session = Depends(get_db),
    token: Optional[str] = Depends(oauth2_scheme)
) -> User:
    # テスト用に常に最初のユーザーを返す
    # 本番環境では適切な認証を実装する必要がある
    user_obj = user.get(db, id=1)
    if not user_obj:
        # ユーザーが存在しない場合は新規作成
        from app.schemas.user import UserCreate
        user_create = UserCreate(email="admin@example.com", password="password")
        user_obj = user.create(db, obj_in=user_create)
    return user_obj
