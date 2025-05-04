from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.crud_item import item
from app.models.user import User
from app.schemas.item import Item, ItemCreate, ItemUpdate

router = APIRouter()

@router.get("/", response_model=List[Item])
def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    全アイテムを取得
    """
    items = item.get_multi(db, skip=skip, limit=limit)
    return items

@router.post("/", response_model=Item)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: ItemCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    新規アイテムを作成
    """
    return item.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)

@router.get("/{id}", response_model=Item)
def read_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    特定のアイテムを取得
    """
    db_item = item.get(db=db, id=id)
    if not db_item:
        raise HTTPException(status_code=404, detail="アイテムが見つかりません")
    return db_item

@router.put("/{id}", response_model=Item)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_in: ItemUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    アイテムを更新
    """
    db_item = item.get(db=db, id=id)
    if not db_item:
        raise HTTPException(status_code=404, detail="アイテムが見つかりません")
    if db_item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="このアイテムを更新する権限がありません")
    return item.update(db=db, db_obj=db_item, obj_in=item_in)

@router.delete("/{id}", response_model=Item)
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    アイテムを削除
    """
    db_item = item.get(db=db, id=id)
    if not db_item:
        raise HTTPException(status_code=404, detail="アイテムが見つかりません")
    if db_item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="このアイテムを削除する権限がありません")
    return item.remove(db=db, id=id)
