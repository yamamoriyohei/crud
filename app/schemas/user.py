from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# 共通属性
class UserBase(BaseModel):
    email: EmailStr

# 作成時に必要な追加属性
class UserCreate(UserBase):
    password: str

# 更新時に使用
class UserUpdate(UserBase):
    password: Optional[str] = None
    is_active: Optional[bool] = None

# DBから取得したデータ
class UserInDBBase(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# APIレスポンス用
class User(UserInDBBase):
    pass

# DB内部用（パスワードハッシュを含む）
class UserInDB(UserInDBBase):
    hashed_password: str
