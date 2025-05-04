from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# 共通属性
class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

# 作成時に必要な追加属性
class ItemCreate(ItemBase):
    title: str
    price: float

# 更新時に使用
class ItemUpdate(ItemBase):
    pass

# DBから取得したデータ
class ItemInDBBase(ItemBase):
    id: int
    title: str
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# APIレスポンス用
class Item(ItemInDBBase):
    pass
